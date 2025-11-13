import polars as pl

salary_question = (
    "What is your monthly salary in DKK, before tax and including pension?"
)

experience_question = (
    "How many years of relevant full-time work experience do you have?"
)

data_2022 = pl.read_csv("Data - 2022.csv", separator=";")
data_2023 = pl.read_csv("Data - 2023.csv")

unpivoted_data_2022 = (
    data_2022.with_row_count(name="user_id")
    .melt(["user_id", "Timestamp", salary_question])
    .select(
        pl.col("user_id"),
        pl.col("variable").alias("question"),
        pl.col("value").alias("answer"),
        pl.col("Timestamp")
        .alias("created_at")
        .str.strptime(pl.Datetime, "%m/%d/%Y %H:%M:%S"),
        pl.col(salary_question)
        .str.replace(".", "", literal=True)
        .str.lstrip("0")
        .str.rstrip(" ")
        .str.replace("", 0, literal=True)
        .alias("monthly_salary")
        .cast(pl.Int64),
    )
).with_columns(pl.lit(2022).alias("year"))

unpivoted_data_2023 = (
    data_2023.with_row_count(name="user_id", offset=len(data_2022))
    .melt(["user_id", "Timestamp", salary_question])
    .select(
        pl.col("user_id"),
        pl.col("variable").alias("question"),
        pl.col("value").alias("answer"),
        pl.col("Timestamp")
        .alias("created_at")
        .str.slice(0, 19)
        .str.strip()
        .str.strptime(pl.Datetime, "%Y/%m/%d %H:%M:%S"),
        pl.col(salary_question)
        .str.replace(".", "", literal=True)
        .str.lstrip("0")
        .str.rstrip(" ")
        .str.replace("", 0, literal=True)
        .alias("monthly_salary")
        .cast(pl.Int64),
    )
).with_columns(pl.lit(2023).alias("year"))

unpivoted_data = pl.concat(
    [
        unpivoted_data_2022,
        unpivoted_data_2023,
    ]
).with_columns(
    [
        pl.col("question").str.rstrip(" ").str.lstrip(" "),
        pl.when(pl.col("question") == experience_question + " ")
        .then(
            pl.col("answer")
            .str.replace(r" years| year", "")
            .str.replace(r"Less than a", "0")
        )
        .otherwise(pl.col("answer").str.rstrip(" ").str.lstrip(" ")),
    ]
)


unpivoted_data.write_parquet("salary_surveys_data.parquet")
unpivoted_data.write_json("salary_surveys_data.json", pretty=True, row_oriented=True)
