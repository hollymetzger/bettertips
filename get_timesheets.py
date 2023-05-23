import os
from square.client import Client

client = Client(
    access_token=os.environ['SQUARE_ACCESS_TOKEN'],
    environment='production')

def get_active_shifts(location_id, time):
    try:
        # List employee wages for all employees at the specified location
        wages = client.team.list_employee_wages(location_ids=[location_id]).employee_wages
        
        # Filter employee wages to only include those with active shifts during the specified time
        active_employee_ids = []
        for wage in wages:
            if wage.employee_id not in active_employee_ids:
                try:
                    # List shifts for this employee during the specified time
                    shifts = client.employees.list_employee_shifts(wage.employee_id, location_ids=[location_id], start= time, end= time).shifts
                    
                    # Check if the employee had an active shift during the specified time
                    for shift in shifts:
                        if shift.is_open:
                            active_employee_ids.append(wage.employee_id)
                            break
                except Exception as e:
                    print("Exception when calling ShiftsApi->list_shifts: %s\n" % e)
        
        # List all shifts for the specified location during the specified time
        shifts = client.shifts.list_shifts(location_ids=[location_id], start= time, end= time).shifts
        
        # Filter shifts to only include those for active employees
        active_shifts = []
        for shift in shifts:
            if shift.employee_id in active_employee_ids:
                active_shifts.append(shift)
        
        return active_shifts
    
    except Exception as e:
        print("Exception when calling API: %s\n" % e)


print(get_active_shifts('locationid', '2023-05-12T15:37:00.828Z'))
