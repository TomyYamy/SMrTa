import json


if __name__ == '__main__':

  file_path_transport_orders = 'benchmarks/potaro/transport_orders_202509111028.json'
  file_path_transport_tasks  = 'benchmarks/potaro/transport_tasks_202509111028.json'

  # Load json
  with open(file_path_transport_orders) as f:
    transport_orders = json.load(f)
  #print(transport_orders)

  with open(file_path_transport_tasks) as f:
    transport_tasks = json.load(f)
  #print(transport_orders)

