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
# transport_type = {1: 薬剤、検体 }
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
  filter_date = datetime.date(2025, 8, 20)

  transport_orders_date_filtered = []
  for transport_order in transport_orders:
    created = datetime.datetime.strptime(transport_order['created'], '%Y-%m-%d %H:%M:%S')
    if filter_date <= created.date() and created.date() < filter_date+datetime.timedelta(days=1):
      transport_orders_date_filtered.append(transport_order)
  #print(transport_orders_date_filtered)

  for transport_order in transport_orders_date_filtered:
    created = datetime.datetime.strptime(transport_order['created'], '%Y-%m-%d %H:%M:%S')
    transport_desired_time = datetime.datetime.strptime(transport_order['transport_desired_time'], '%Y-%m-%d %H:%M:%S')
    #print(f'issued time={created} deadline={transport_desired_time}')
    #print(transport_order['od_list'])

    ## find order_id in transport_tasks
    transport_tasks_matched = [ transport_task for transport_task in transport_tasks if transport_task['order_id'] == transport_order['order_id'] ]
    if transport_order['transport_type'] == 1:
      print(transport_order['transport_type'])
      print(f'tasks num = {len(transport_tasks_matched)}')
      print(transport_tasks_matched)
    #print(transport_tasks_searched)


  #for transport_task in transport_tasks:
  #  print(transport_tasks)
