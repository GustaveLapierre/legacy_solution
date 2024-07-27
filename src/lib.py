import io
import pandas as pd


def get_data_structure_from_excel_file(
    fp: io.BytesIO, sheet_name: str = "Sheet1", file_type: str = "xlsx" or "xls" or "csv"
) -> list[dict] | None:
    """
        This function reads an excel or csv file and returns a list of dictionaries.
        Each dictionary represents a data structure that contains a general question,
        specific questions and notes.

    Args:
        fp (io.BytesIO): The excel file to be read.
        sheet_name (str, optional): The name of the sheet to be read. Defaults to "Sheet1".
        file_type (str, optional): The type of the file. Defaults to "xlsx".

    Returns:
        list[dict] | None: A list of dictionaries representing the data structure or None if an error occurs.
    """
    try:
        if file_type == "csv":
            df = pd.read_csv(fp, encoding="utf-8")
        else:
            df = pd.read_excel(fp, sheet_name=sheet_name)

        # list to store result
        result = []

        for index, row in df.iterrows():
            if not pd.isna(row["General Question"]):
                current_dict = {
                    "General Question": row["General Question"],
                    "Specific Questions": row["Specific Questions"],
                    "Notes": [
                        {key: value if not pd.isna(value) else ""}
                        for key, value in row[2:].items()
                    ],
                }

                result.append(current_dict)
            else:
                # due to the way the data is structured, NaN values for General Question are either
                # replaced with the last value for General Question or with literal "General Question".
                last_dict_item = result[-1]
                current_dict = {
                    "General Question": last_dict_item["General Question"]
                    or "General Question",
                    "Specific Questions": row["Specific Questions"],
                    "Notes": [
                        {key: value if not pd.isna(value) else ""}
                        for key, value in row[2:].items()
                    ],
                }
                result.append(current_dict)

        return result
    except Exception as e:
        print("Error: ", e)
        # print(traceback.format_exc()) #! For debugging, in Debug mode
        return None
