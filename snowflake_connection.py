import snowflake.connector

conn = snowflake.connector.connect(
    account="UK63233.ap-southeast-7.aws",
    user="MARVINEBREOMAGTIBAY",
    authenticator="OAUTH_AUTHORIZATION_CODE",
    role="ACCOUNTADMIN",
    warehouse="SNOWFLAKE_LEARNING_WH",
    database="PROJECT1_DB",
    schema="DEPARTMENT",
    client_store_temporary_credential=True
)