from traffic import get_nh65_traffic_route
import json

routes = get_nh65_traffic_route()
print(json.dumps(routes, indent=2))
