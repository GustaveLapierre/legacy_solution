import os
import re
from openai import OpenAI
from src.models import Entries, GeneralSummary, db
from src.utils import concat_summaries
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

SYSTEM_PROMPT = """
You are a helpful assistant. You will be given some text in English or French.\
You are to generate summaries from the text as well as a short quote from the\
corresponding section of the text that directly supports the summary which would\
be used as quote. Also generate a 2-3 word suitable title for the summary.\
Always retain the source language of the text when generating the summary, \
i.e. if it is in significantly English, then the summary should be in English, \
if it is in French, then the summary should be in French and so on. \
Do not respond with anything else other the response in this exact format:\n
+==Summary==+
{summary}
+==Summary==+

+==Title==+
{title}
+==Title==+

+==Quote==+
{quote}
+==Quote==+
"""

GENERAL_SUMMARY_SYSTEM_PROMPT = """
You are a helpful assistant. You will be given some text. \
You are to summarize the whole text into a single, relatively short sentence or paragraph.\
This sequence of literal new line characters "\n\n\n" indicates that the next part of the 
sentence might be another point, consider this in your summary as well. Always retain the source \
language of the text when generating the summary, i.e. if it is significantly in English, then the summary \
should be in English, if it is in French, then the summary should be in French and so on. \
Do not respond with anything else other the response in this exact format:\n
+==Summary==+
{summary}
+==Summary==+
"""

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY must be set")


def prepare_data_for_summary(data: list[dict], min_length: int = 120):
    """
    Prepare data for summary, striping out notes that are too short.
    """
    result = []
    for items in data:
        filtered_notes = []
        for notes in items["Notes"]:
            for _, value in notes.items():
                if len(value) >= min_length:
                    filtered_notes.append(notes)
                    break
        items["Notes"] = filtered_notes
        result.append(items)

    return result


def format_gpt_response(response):
    """
    Extract summary, title and quote from GPT response.
    """
    result = {}
    summary_pattern = r"\+==Summary==\+\n(.*?)\n\+==Summary==\+"
    quote_pattern = r"\+==Quote==\+\n(.*?)\n\+==Quote==\+"
    title_pattern = r"\+==Title==\+\n(.*?)\n\+==Title==\+"

    summary_match = re.search(summary_pattern, response, re.DOTALL)
    if summary_match:
        result["summary"] = summary_match.group(1).strip()
    else:
        result["summary"] = ""

    quote_match = re.search(quote_pattern, response, re.DOTALL)
    if quote_match:
        result["quote"] = quote_match.group(1).strip()
    else:
        result["quote"] = ""

    title_match = re.search(title_pattern, response, re.DOTALL)
    if title_match:
        result["title"] = title_match.group(1).strip()
    else:
        result["title"] = ""

    return result


def generate_summary(record_id: str, data: list[dict]) -> bool | None:
    """
    Generate summaries for each note in the given data for the specified record.

    Args:
        record_id (str): The ID of the record.
        data (list[dict]): The list of dictionaries containing the notes to summarize.
            Each dictionary should have the following keys:
            - "General Question" (str): The general question.
            - "Specific Questions" (str): The specific questions.
            - "Notes" (list[dict]): The list of notes.
                Each note is a dictionary with the following keys:
                - Any key (str): The value of the note.

    Returns:
        bool | None: True if the summaries were generated successfully, None otherwise.

    Raises:
        Exception: If an error occurs during the summary generation process.
    """

    try:
        client = OpenAI(api_key=OPENAI_API_KEY)

        print("Starting Summary Generation...")
        # loop through each note in data
        # check if note is long enough to summarize

        for item in prepare_data_for_summary(data):
            # Create a new entry
            entry: Entries = Entries()

            # add necessary defaults to entry
            entry.record_id = record_id
            entry.title = item["General Question"]
            # entry.subtitle = item["Specific Questions"]

            # loop through each note
            for note in item["Notes"]:
                for _, value in note.items():
                    # send value to OpenAI for summary
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": value},
                        ],
                        model="gpt-4o",
                        max_tokens=4095,
                    )

                    # save summary and quote to entry
                    response = format_gpt_response(
                        chat_completion.choices[0].message.content
                    )
                    # print(response)  #! DEBUG
                    entry.summary = response["summary"]
                    entry.subtitle = response["title"]
                    entry.quote = response["quote"]

                # add entry to database and commit
                db.session.add(entry)
                db.session.commit()
        # print("Done")  #! DEBUG

        # concatenate summaries
        concatenated_summaries = concat_summaries(record_id)
        # loop through each summary, and generate general summary
        for summary in concatenated_summaries:
            # create general summary
            general_summary: GeneralSummary = GeneralSummary()
            general_summary.record_id = record_id
            general_summary.title = summary["key"]

            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": GENERAL_SUMMARY_SYSTEM_PROMPT},
                    {"role": "user", "content": summary["value"]},
                ],
                model="gpt-4o",
                max_tokens=4095,
            )
            response = format_gpt_response(chat_completion.choices[0].message.content)
            general_summary.summary = response["summary"]
            db.session.add(general_summary)
            db.session.commit()

        return True

    except Exception as e:
        print(e)  #! DEBUG
        return None
