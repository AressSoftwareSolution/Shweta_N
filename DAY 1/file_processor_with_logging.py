import logging
logging.basicConfig(filename='file_processor.log', level=logging.INFO)

logging.info("file processor is started")
logging.info("performing a file handling operation")
try:
    with open("sample.txt", "r") as f:
        content= f.read()
        logging.info(" read successfully.")
except FileNotFoundError:
    logging.error("File 'sample.txt' not found.")
except Exception as e:
    logging.error(f"An error occurred: {e}")

try:
    with open("sample2.txt","a") as f:
        f.write("\n new content added")
        logging.info("content appended sucessfully")
except Exception as e:
    logging.error(f"an error occurred:{e}")
