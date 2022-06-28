from google.cloud import bigquery

DATASET = "IP_Trackingvn"


def load(table: str, partition_key: str, schema: list[dict]):
    def _load(rows: list[dict]) -> int:
        client = bigquery.Client()
        output_rows = (
            client.load_table_from_json(
                rows,
                f"{DATASET}.{table}",
                job_config=bigquery.LoadJobConfig(
                    schema=schema,
                    create_disposition="CREATE_IF_NEEDED",
                    write_disposition="WRITE_APPEND",
                    time_partitioning=bigquery.TimePartitioning(
                        type_=bigquery.TimePartitioningType.DAY,
                        field=partition_key,
                    ),
                ),
            )
            .result()
            .output_rows
        )

        return output_rows

    return _load
