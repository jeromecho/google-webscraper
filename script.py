from jobs.Job import Job
from filters.Filter import Filter

jobs: list[Job] = []

ripe_apples_filters = [
  Filter("recipe"),
  Filter("woman"),
  Filter("man"),
  Filter("person"),
  Filter("chart"),
  Filter("art"),
  Filter("pie")
]
ripe_apples_job = Job(query_string="ripe apples", filters=ripe_apples_filters, save_dir="apples_ripe")

unripe_apples_filters = [
  Filter("webtoon"),
  Filter("after school lessons"),
  Filter("afterschool"),
  Filter("youths"),
  Filter("make")
].extend(ripe_apples_filters)
unripe_apples_job = Job(query_string="unripe apples", filters=unripe_apples_filters, save_dir="apples_unripe")

ripe_blueberries_filters = [
].extend(ripe_apples_filters)
ripe_blueberries_job = Job(query_string="ripe blueberries", filters=ripe_blueberries_filters, save_dir="blueberries_ripe")

unripe_blueberries_filters = [
  Filter("ripe")
].extend(ripe_apples_filters)
unripe_blueberries_job = Job(query_string="unripe bluberries", filters=unripe_blueberries_filters, save_dir="blueberries_unripe")

jobs.append(ripe_apples_job)
jobs.append(unripe_apples_job)
jobs.append(ripe_blueberries_job)
jobs.append(unripe_blueberries_job)

for job in jobs:
  job.run()
