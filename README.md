<h2>EVEnergy real time problem</h2>

In this readme I have written most of my thoughts during my thinking time for the task. I must admit that it was real pleasure and true challenge thinking for possible solution about this complex task. Furthermore, knowing its real time problem, it challenges me to work on and solve it.

<h4>Task notes</h4>

Since the time spent on this task is supposed to be 2-3 hours, I'm not providing full code solution, nor any devops support (i.e. dockerized solution).
There are probably many ways how this problem could be solved. I took liberty to split the problem and create models for possible solution. 
Note: Models are just skeleton representation of the task, created after the first reading of the task.
Regarding the UI, the simplest will be to use django admin to represent scheduling times.

<h5>Things to be clarified:</h5>

1. In the task description it's mentioned `27th of September` as plug_in_time, but in the data another date time is mentioned. I.e. `plug_in_time='2019-10-04T18:42:12+00:00')`. I assume this is mistake?
2. To make time zone aware schedules we can save data in utc and convert in timezone depending on the need. - Excellent library that makes this really easy to handle is `Arrow library`. We use it on our existing project in the company when we gather real-time measurements from solar fields and it's really great.

Because this is really complex problem that needs time and some priorities set before actual job is done, I have thought of few possible solutions:

First scenario:
Enid has `Go tariff`. This means it will be cheapest for her to charge the car between `00:30 - 7:30` in the morning. Taking into consideration her schedule and the fact that she lives somewhere on the North, we can conclude it will be most efficient the car to be turned off from charging at `7:00AM`.
Next condition is the CO2 emission index. We should check at what time the CO2 emission index is lowest according to our forecast.
- `energy_supplier_tariff = 'Go tariff'`
- `ready_by = '7:00'`
- `charge_time = 300 = 5h`
- `efficient_charge_from = '00:30'.` 
Here we can use the plug_in_time variable to calculate for which day we are generating schedules.plug_in_time='2019-10-04T18:42:12+00:00' means that the charging interval
should be from '2019-10-05T00:30:00+00:00' to '2019-10-05T07:30:00+00:00'
- `efficient_charge_to = '7:30'`
- `emission_index = data["intensity"]["forecast"]`

[comment]: <> (    time_interval is list of 30 min intervals in the period between efficient_charge_from and ready_by.)

```
generate_green_charging_schedule(ready_by='07:00', charge_time=300, plug_in_time='2019-10-04T18:42:12+00:00'):
    for every time_interval in range(efficient_charge_from, ready_by):
        find_coresponding_interval in carbon_intensity_json and check:
            if emission_index = data["intensity"]["index"] is 'low':
                print(f"Green charge interval: {time_interval}")
```
- I was also thinking of generating time schedules of 300 min duration, but this somehow doesn't make sense. We have carbon_emission slots of 30 minutes which if we want to use as a condition, we'll need exactly same charging slots, otherwise the forecast will not have any effect.
-We also need to keep `charge_time` parameter updated once the time slot was picked.
 
  
Second scenario adds up on the first and makes really efficient, but much more complex solution:
- `If we take into consideration battery_level. I.e 10, 50, 80 % full etc, we can re-calculate charging time, which won't be 300 minutes but less.`
- `Example: battery_level = 80%`
- `charge_time = 300 minutes - time_needed_to_charge_last_20%` 
- `Next steps are same as in the first scenario`

Third scenario, IMO even more complex, will be extension on the second case. Here we can assume that the car can be charged multiple times in shorter intervals, but instead of the data["intensity"]["index"], we will use data["intensity"]["forecast"]. 
- `If charge_time = 60; battery_level = 80%;`

```
def generate_green_charging_schedule(ready_by='07:00', charge_time=300, plug_in_time='2019-10-04T18:42:12+00:00'):
    if charge_time > 0 and battery_level < 100 %:
        plug_in_time='2019-10-04T18:42:12+00:00'
        efficient_charge_from = '00:30 plus the next day derived from plug_in_time.date'
        list_of_30_min_charge_intervals = range(efficient_charge_from, ready_by) 
        number_of_charging_intervals = (charge_time/30).count()
        cross-match the 2 lists: list_of_30_min_charge_intervals and carbon_emission_json and get the data only
        for the matching intervals
        order the retrieved data by asc data["intensity"]["forecast"] parameter
        select the first n results from the ordered data, where n = number_of_charging_intervals

```
