# DepthToInundationPts is a class object which identifies the
# intersection between National Hydrologic Dataset vectors (i.e.
# streams) and National Transportation Dataset vectors (i.e. roads,
# railways, trails). These intersections are then buffered by 100 m.
# Buffers are then used to clip the transportation routes. Offset lines
# are created from the clipped transportation routes. Elevations,
# from the Best Available Topographic (BAT) Dataset, are then extracted
# at the vector data's vertecies. The minimum elevation on each offset
# line is then identified and the nearest point along the road. These
# elevations are differenced resulting in delta z or depth-to-inudation.
#
# Author: John Wall (jwall@Dewberry.com)
#
# Copyright: Dewberry
#
# ----------------------------------------------------------------------

import pandas as pd
from matplotlib import pyplot as plt
import geopandas as gpd
import shapely
from shapely import geometry, ops
from shapely.geometry import Point, LineString
from shapely.ops import nearest_points
import rasterio
from rasterio.plot import show
from rasterstats import zonal_stats, point_query

# Helper functions
def create_3d_pnt(pnt, dem):
    '''Creates a z-enabled point from a 2d pnt and elevation data.'''
    z = point_query(pnt, dem)[0]
    try:
        x, y, _ = list(pnt.coords)[0]
    except:
        print("2d point provided")
        x, y = list(pnt.coords)[0]
    return Point([x,y,z])

def pachinko(pnt1, pnt2):
    '''Determines start and end points based on elevation.'''
    coords1 = list(pnt1.coords)[0]
    coords2 = list(pnt2.coords)[0]
    lower, upper = sorted([coords2, coords1], key=lambda pnt: pnt[2])
    return Point([lower]), Point([upper])

def validate_strm_orentation(stream_line, dem):
    strm_len = stream_line.length
    
    pnt1 = Point([list(stream_line.coords)[0]])
    pnt2 = Point([list(stream_line.coords)[-1]])

    pnt1_3d = create_3d_pnt(pnt1, dem)
    pnt2_3d = create_3d_pnt(pnt2, dem)

    end_pnt, start_pnt = pachinko(pnt1_3d, pnt2_3d)
    
    if strm_len != stream_line.project(end_pnt):
        raise Exception("WARNING: Stream end point does not match stream length!")

class DepthToInundationPts(object):
    """Geospaital points representing the cartographic location of
        lowest elevation (i.e. channel) at a transportation-route-stream
        intersection. The point is attributed with the difference in
        elevation between the top of the transporation route and
        the channel elevation.
        
       Parameters:
        streams (str): Path to streams as vectors
        transit_routes (str): Path to roads as vectors
        dem (str): Path to a digitial elevation model as raster
        prj (dict): Projection information
    """
    def __init__(self, streams, transit_routes, dem, prj):
        
        def load_data(data, prj, data_type):
            """Loads data into the object based on dataset type (i.e.
                streams, roads, etc.). Can easily be extended to
                include other types.
            """
            rprj_data = gpd.read_file(data).to_crs(prj)
            if data_type == "streams":
                return rprj_data
            elif data_type == "roads":
                return rprj_data.dissolve(by='FULL_STREE')
            else:
                print("Neither streams nor roads.")

        def find_intersections(self):
            """Finds intersections between *A* stream and
                transportation routes.

                THIS FUNCTION NEEDS TO BE REWRITTEN TO EXECUTE OVER ALL
                STREAMS OF INTEREST.
            """
            stream_shape = self._streams.geometry[0]
            routes = self._routes
            possible_intersections = routes.geometry.apply(lambda row: stream_shape.intersection(row))
            return possible_intersections[~possible_intersections.is_empty]
        
        def clip_transit_routes(self):
            """Clips transportation routes, converts them to single
                parts,explodes the results to account for routes
                with the same name. Contains logic to ensure only
                records with geospatial data are return.
            """
            clp_routes = self._intxn_polys.intersection(self._routes)

            single_lines = {}
            for i, transit in enumerate(clp_routes):
                if 'GeometryCollection' not in type(transit).__name__ :
                    if type(transit) is shapely.geometry.multilinestring.MultiLineString:
                        single_lines[clp_routes.index[i]] = ops.linemerge(transit)
                    else:
                        single_lines[clp_routes.index[i]] = transit

            columns=['transit','geometry']
            explode_lines = gpd.GeoDataFrame(single_lines.items(), columns=columns)
            try:
                return explode_lines.explode().droplevel(0).reset_index(0, drop=True)
            except:
                return explode_lines
        
        def create_offsets(self):
            """Creates left and right offset profile lines from clipped
                transportation routes.
            """
            clp_roads = self._clp_roads.copy()
            strm = self._streams.geometry[0] # Currently only working with a single stream

            gdf_upstream = gpd.GeoDataFrame(columns=['transit','geometry','side','offset'])
            gdf_downstream = gpd.GeoDataFrame(columns=['transit','geometry','side','offset'])

            validate_strm_orentation(strm, self._dem)

            for i, idx in enumerate(clp_roads.index):
                road_name = clp_roads.loc[idx].transit
                road = clp_roads.loc[idx].geometry

                offsets = [road.parallel_offset(100, side, resolution=1) for side in ['left', 'right']]
                offset_intx = [strm.intersection(offset) for offset in offsets]
                dists = [strm.project(intx) for intx in offset_intx]

                gdf_upstream.loc[i, 'transit'] = road_name
                gdf_upstream.loc[i, 'geometry'] = road

                gdf_downstream.loc[i, 'transit'] = road_name
                gdf_downstream.loc[i, 'geometry'] = road

                if dists.index(min(dists)) == 0:
                    gdf_upstream.loc[i, 'side'] = 'upstream'
                    gdf_upstream.loc[i, 'offset'] = offsets[0]
                    gdf_downstream.loc[i, 'side'] = 'downstream'
                    gdf_downstream.loc[i, 'offset'] = offsets[1]
                else:
                    gdf_upstream.loc[i, 'side'] = 'upstream'
                    gdf_upstream.loc[i, 'offset'] = offsets[1]
                    gdf_downstream.loc[i, 'side'] = 'downstream'
                    gdf_downstream.loc[i, 'offset'] = offsets[0]

            return pd.concat([gdf_upstream, gdf_downstream]).reset_index(0, drop=True)
        
        def create_topographic_profiles(self, column):
            """Updates 2d lines to 3d topographic profiles"""
            lns = self._offset_lines
            for i in lns.index:
                profile_points = point_query(lns[column][i], dem)[0]
                points3d = []
                for ii, z in enumerate(profile_points):
                    x, y = list(lns[column][i].coords)[ii]
                    points3d.append(Point([x,y,z]))
                lns.loc[i][column] = LineString(points3d)
            return lns
        
        def identify_line_minimum(self, column, idx = None):
            """Identifies the minimum on a 3d line"""
            gdf = self._offset_profiles
            verticies = gdf[column].apply(lambda line: line.coords)
            z_values = verticies.apply(lambda line_verticies: [vertex[2] for vertex in line_verticies])
            minima = z_values.apply(lambda z_value: min(z_value))
            out_column_name = '_'.join([column,'min'])
            if idx is not None:
                gdf.insert(loc=idx, column=out_column_name, value=minima)
            else:
                gdf[out_column_name] = minima
            return gdf
        
        def get_deltas(self):
            """Calculate difference in height between routes and offset profiles"""
            gdf = self._route_minima
            gdf['delta_z'] = gdf.geometry_min - gdf.offset_min
            return gdf
        
        # Basic, input properties
        self._streams = load_data(streams, prj, "streams")
        self._routes = load_data(transit_routes, prj, "roads")
        self._dem = dem
        
        # Computed properties
        self._intxn_points = find_intersections(self)
        self._intxn_polys = self._intxn_points.buffer(100)
        self._clp_roads = clip_transit_routes(self)
        self._offset_lines = create_offsets(self)
        self._offset_profiles = create_topographic_profiles(self, 'offset')
        self._route_profiles = create_topographic_profiles(self, 'geometry')
        self._offset_minima = identify_line_minimum(self, 'offset')
        self._route_minima = identify_line_minimum(self, 'geometry', 2)
        self._deltas = get_deltas(self)
    
    @property
    def gdf_streams(self):
        """GeoPandas GeoDataFrame of Streams"""
        return self._streams
    
    @property
    def gdf_routes(self):
        """GeoPandas GeoDataFrame of Transportation routes"""
        return self._routes
    
    @property
    def dem(self):
        """Digitial Elevation Model used to cross section creation"""
        return self._dem
    
    @property
    def intersection_points(self):
        """Stream and transportation intersection points"""
        return self._intxn_points
    
    @property
    def intersection_polygons(self):
        """Buffers around intersection points"""
        return self._intxn_polys
    
    @property
    def clipped_roads(self):
        """Transportation routes clipped to buffers"""
        return self._clp_roads
    
    @property
    def offset_lines(self):
        """Lines offset from the clipped transportation route"""
        return self._offset_lines
    
    @property
    def offset_profiles(self):
        """Offset topographic profiles"""
        return self._offset_profiles
    
    @property
    def route_profiles(self):
        """Route topographic profiles"""
        return self._route_profiles
    
    @property
    def offset_minima(self):
        """Minima of offset topographic profiles"""
        return self._offset_minima
    
    @property
    def route_minima(self):
        """Minima of route topographic profiles"""
        return self._route_minima
    
    @property
    def delta_z(self):
        """Difference in height between min(route) and min(offset)"""
        return self._deltas