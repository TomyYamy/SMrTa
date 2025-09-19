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


id_exchange_dic = {
  '020100318': '020100316'
}
no_exist_in_weighted_graph = ['020100610', '020100408', '020100729', '020100724', '020100605', '020100829', '020100910', '020100318', '020100419', '020100805', '020100206', '020100202', '020100905', '020100209', '020100629', '020100705', '020100824']


if __name__ == '__main__':

  file_path_transport_orders = 'benchmarks/potaro/transport_orders_202509111028.json'
  file_path_transport_tasks  = 'benchmarks/potaro/transport_tasks_202509111028.json'
  num_agents = 4
  filter_date = datetime.date(2025, 8, 20)
  offset_time = datetime.timedelta(hours=2)
  incremental_time_period = datetime.timedelta(minutes=30)

  # Load json
  with open(file_path_transport_orders) as f:
    transport_orders = json.load(f)['transport_orders']
  #print(transport_orders)

  with open(file_path_transport_tasks) as f:
    transport_tasks = json.load(f)['transport_tasks']
  #print(transport_orders)

  transport_orders_date_filtered = []
  for transport_order in transport_orders:
    created = datetime.datetime.strptime(transport_order['created'], '%Y-%m-%d %H:%M:%S')
    transport_desired_time = datetime.datetime.strptime(transport_order['transport_desired_time'], '%Y-%m-%d %H:%M:%S')
    if (filter_date <= created.date() and created.date() < filter_date+datetime.timedelta(days=1)-offset_time) and (filter_date <= transport_desired_time.date() and transport_desired_time.date() < filter_date+datetime.timedelta(days=1)-offset_time):
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
  test_case = []
  for transport_order in transport_orders_device_id_filtered:
    created = datetime.datetime.strptime(transport_order['created'], '%Y-%m-%d %H:%M:%S')
    transport_desired_time = datetime.datetime.strptime(transport_order['transport_desired_time'], '%Y-%m-%d %H:%M:%S')
    #print(f'issued time={created} deadline={transport_desired_time}')
    #print(f'num of od list = {len((ast.literal_eval(transport_order['od_list'])[0]))}')
    print(f'od_list = {transport_order['od_list']}')
    # Note: od_list struct
    #[[[{'global_id': '020100318'}],
    #  [{'global_id': None}]],
    # [[{'global_id': None}],
    #  [{'global_id': '020100316'}]]]

    ## find order_id in transport_tasks
    transport_tasks_matched = [ transport_task for transport_task in transport_tasks if transport_task['order_id'] == transport_order['order_id'] ]
    #print(f'matched tasks num = {len(transport_tasks_matched)}')
    #print(f'Matched tasks = {transport_tasks_matched}')
    # Note: Matched tasks
    #[{'task_id': '083953de-8a7d-466c-907e-737a780d868d', 'order_id': 'fe71f30d-1096-4d1c-840c-c488ea996908', 'sequence_number': 4, 'task_sequence_total_count': 4, 'device_id': '0001-011301-000002', 'task_type': 'PICK_DOWN', 'task_object': "['薬剤']", 'destination': "['020100316','荷下完了']", 'task_status': '実行完了', 'deleted': None, 'created': '2025-08-20 18:49:58', 'created_user': None, 'modified': '2025-08-20 19:02:49', 'modified_user': None},
    # {'task_id': '2bbfe948-8ca5-418e-918d-d8bd0746ad5f', 'order_id': 'fe71f30d-1096-4d1c-840c-c488ea996908', 'sequence_number': 3, 'task_sequence_total_count': 4, 'device_id': '0001-011301-000002', 'task_type': 'PICK_UP', 'task_object': "['薬剤']", 'destination': "['020100709','積荷完了']", 'task_status': '実行完了', 'deleted': None, 'created': '2025-08-20 18:49:58', 'created_user': None, 'modified': '2025-08-20 18:58:07', 'modified_user': None}, 
    # {'task_id': '6a1b6e93-d906-444e-be4f-6608b665c893', 'order_id': 'fe71f30d-1096-4d1c-840c-c488ea996908', 'sequence_number': 1, 'task_sequence_total_count': 4, 'device_id': '0001-011301-000002', 'task_type': 'PICK_UP', 'task_object': "['薬剤']", 'destination': "['020100318','積荷完了']", 'task_status': '実行完了', 'deleted': None, 'created': '2025-08-20 18:49:58', 'created_user': None, 'modified': '2025-08-20 18:52:06', 'modified_user': None}, 
    # {'task_id': 'd9e56ab2-838c-464a-91e1-1241eff0c899', 'order_id': 'fe71f30d-1096-4d1c-840c-c488ea996908', 'sequence_number': 2, 'task_sequence_total_count': 4, 'device_id': '0001-011301-000002', 'task_type': 'PICK_DOWN', 'task_object': "['薬剤']", 'destination': "['020100708','荷下完了']", 'task_status': '実行完了', 'deleted': None, 'created': '2025-08-20 18:49:58', 'created_user': None, 'modified': '2025-08-20 18:56:47', 'modified_user': None}]

    ## Skip empty box pick up.
    if len(transport_tasks_matched) == 3 or len(transport_tasks_matched) == 4:
      ## find sequence_number = 1 and 2 as start and target.
      task_sequence_number_1 = [ transport_task for transport_task in transport_tasks_matched if transport_task['sequence_number'] == 1 ]
      task_sequence_number_1 = task_sequence_number_1[0]
      print(f'start_task = {task_sequence_number_1}')
      task_sequence_number_2 = [ transport_task for transport_task in transport_tasks_matched if transport_task['sequence_number'] == 2 ]
      task_sequence_number_2 = task_sequence_number_2[0]
      print(f'target_task = {task_sequence_number_2}')

      start  = ast.literal_eval(task_sequence_number_1['destination'])[0]
      target = ast.literal_eval(task_sequence_number_2['destination'])[0]
      if (target == 'to_be_determined'):
        print(f'{transport_order['od_list']} is skipped, due to skipped task.')
        continue
    else:
      print(f'{transport_order['od_list']} is skipped, due to different task.')
      continue

    ## add test case
    test_case.append({'from': start, 'to': target, 'deadline': transport_desired_time, 'issued_time': created})

  # Show test case
  print(f'--test case # is {len(test_case)} --')
  for order in test_case:
    print(order)

  # Revise test case
  ## remap several IDs
  test_case_rev = []
  for order in test_case:
    if id_exchange_dic.get(order['from']) != None:
      order['from'] = id_exchange_dic[order['from']]
    if id_exchange_dic.get(order['to']) != None:
      order['to'] = id_exchange_dic[order['to']]
    test_case_rev.append(order)

  ## remove no_exist_in_weighted_graph cases
  test_case_rev = [ order for order in test_case_rev
                    if(order['from'] not in no_exist_in_weighted_graph) and (order['to'] not in no_exist_in_weighted_graph)]

  ## add large value when the dead line is too tight.
  for order in test_case_rev:
    if order['deadline'] - order['issued_time'] < datetime.timedelta(minutes=1):
      order['deadline'] = order['issued_time'] + offset_time

  ## Sort with issued time
  test_case_rev = sorted(test_case_rev, key=lambda x: x['issued_time'])

  print(f'--test case rev # is {len(test_case_rev)} --')
  for order in test_case_rev:
    print(order)

  # Make enumeration of start and goal start_and_goal_candidate_list.
  start_and_goal_candidates = []
  for order in test_case_rev:
    start_and_goal_candidates.append(order['from'])
    start_and_goal_candidates.append(order['to'])
  start_and_goal_candidates = list(set(start_and_goal_candidates))
  start_and_goal_candidates.sort()
  start_and_goal_candidate_list = [ (start_and_goal_candidates[i], i) for i in range(len(start_and_goal_candidates))]
  print(f'start_and_goal_candidate_list = {start_and_goal_candidate_list}')

  # Covert to SMrTa task json.
  test_case_SMrTa = {'tasks_stream': [],
                     'agents': [ i for i in range(num_agents)]}
  incremental_time_count = 1
  temp_tasks = []
  for order in test_case_rev:
    issued_time_minutes = int((order['issued_time']-datetime.datetime.combine(filter_date, datetime.time()))/datetime.timedelta(minutes=1))
    start_id = [ start_and_goal_candidate[1] for start_and_goal_candidate in start_and_goal_candidate_list if start_and_goal_candidate[0]==order['from'] ][0]
    end_id   = [ start_and_goal_candidate[1] for start_and_goal_candidate in start_and_goal_candidate_list if start_and_goal_candidate[0]==order['to']   ][0]
    deadline_minutes = int((order['deadline']-datetime.datetime.combine(filter_date, datetime.time()))/datetime.timedelta(minutes=1))
    task = {'start': start_id,
            'end': end_id,
            'deadline': deadline_minutes}
    if incremental_time_period == None:
      test_case_SMrTa['tasks_stream'].append(
        {
          'arrival': issued_time_minutes,
          'tasks': [task]
        }
      )
    else:
      incremental_time = int(incremental_time_period*incremental_time_count/datetime.timedelta(minutes=1)) # TODO: fix time management without int
      if issued_time_minutes < incremental_time:  # cache task until reach incremental_time
        temp_tasks.append(task)
      else: # store cached tasks
        test_case_SMrTa['tasks_stream'].append(
          {
            'arrival': incremental_time,
            'tasks': temp_tasks
          }
        )
        # increment
        temp_tasks = [task]
        incremental_time_count = incremental_time_count + 1

  print(test_case_SMrTa)

  with open('benchmarks/potaro/test_case4log.json', 'w') as f:
    f.write(json.dumps(test_case_SMrTa, indent=2))
