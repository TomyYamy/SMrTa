# memo
#
# - transport_order
# order_id
# device_id
# ward_setting_id_list
# transport_desired_time
# order_start_time
# status
# od_list
# transport_type
# reservation_datetime
# metomass_reservation_id
# device_seq_number
# arrival_time
# tanto_cd
# arrival_confirmation
# deleted
# created
# created_user
# modified
# modified_user

import datetime
import json


if __name__ == '__main__':

  file_path_transport_orders = 'benchmarks/potaro/transport_orders_202509111028.json'
  file_path_transport_tasks  = 'benchmarks/potaro/transport_tasks_202509111028.json'

  # Load json
  with open(file_path_transport_orders) as f:
    transport_orders = json.load(f)['transport_orders']
  #print(transport_orders)

  with open(file_path_transport_tasks) as f:
    transport_tasks = json.load(f)['transport_tasks']
  #print(transport_orders)

  # filter orders
  filter_date = datetime.date(2025, 8, 25)

  for transport_order in transport_orders:
    created = datetime.datetime.strptime(transport_order['created'], '%Y-%m-%d %H:%M:%S')
    print(created)

  #for transport_task in transport_tasks:
  #  print(transport_tasks)
