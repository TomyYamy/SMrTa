# memo
#
# - transport_order
# order_id
# device_id
#        0001-011701-000005 011701系検体、　0001-011301-000002
# ward_setting_id_list
# transport_desired_time
# order_start_time
# status
# od_list
# transport_type = {1:薬剤、検体随時便 2:スピッツ、検体定時便 3:ME搬送} 1 is anything else of 2 and 3. This time resolves 1 and 3.
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
#
# - transport_tasks
# task_id
# order_id
# sequence_number
# task_sequence_total_count
# device_id
# task_type
# task_object
# destination
# task_status
# deleted
# created
# created_user
# modified
# modified_user


import datetime
import ast
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

  # Filter orders with Date
  filter_date = datetime.date(2025, 8, 20)

  transport_orders_date_filtered = []
  for transport_order in transport_orders:
    created = datetime.datetime.strptime(transport_order['created'], '%Y-%m-%d %H:%M:%S')
    if filter_date <= created.date() and created.date() < filter_date+datetime.timedelta(days=1):
      transport_orders_date_filtered.append(transport_order)
  #print(transport_orders_date_filtered)

  # Filter task type. else specimen　-011701-
  # device_id *-011701-* means specimen
  transport_orders_device_id_filtered = []
  for transport_order in transport_orders_date_filtered:
    if transport_order['device_id'] != None: #Note: sometimes the id has None...
      if '-011701-' not in transport_order['device_id']:
        transport_orders_device_id_filtered.append(transport_order)

  # Resolve destination while matching transport_tasks
  for transport_order in transport_orders_device_id_filtered:
    created = datetime.datetime.strptime(transport_order['created'], '%Y-%m-%d %H:%M:%S')
    transport_desired_time = datetime.datetime.strptime(transport_order['transport_desired_time'], '%Y-%m-%d %H:%M:%S')
    #print(f'issued time={created} deadline={transport_desired_time}')
    print(f'num of od list = {len((ast.literal_eval(transport_order['od_list'])[0]))}')
    print(transport_order['od_list'])
    # Note: od_list struct
    #[[[{'global_id': '020100318'}],
    #  [{'global_id': None}]],
    # [[{'global_id': None}],
    #  [{'global_id': '020100316'}]]]

    ## find order_id in transport_tasks
    transport_tasks_matched = [ transport_task for transport_task in transport_tasks if transport_task['order_id'] == transport_order['order_id'] ]
    if transport_order['transport_type'] == 3:
      print(transport_order['transport_type'])
      print(f'tasks num = {len(transport_tasks_matched)}')
      print('Matched tasks')
      print(transport_tasks_matched)


  #for transport_task in transport_tasks:
  #  print(transport_tasks)
