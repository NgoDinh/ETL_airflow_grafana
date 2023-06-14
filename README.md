### In this section I cover some main topic of airflow:
- xcom_dag: how to push and pull data between task in DAG
- producer and consumer: how to using attribute of one file to trigger a task (producer create a file and when it done will trigger consumer task)
- group_dag: how to combine multi task in a group to make our dag clear and easy to read
- eng to end user processing: combine http operator, python operator and sensor
### To monitor:
- Statsd-exporter to export airflow metric to prometheus
- Time series database: prometheus
- Dashboard to monitoring: Grafana
![Grafana dashboard](/grafana.png)