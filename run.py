import gradio as gr
import cv2
import pandas as pd

try:
    from docreader import DocReader

    reader = DocReader()
    MODEL_LOADED = True
except Exception as e:
    MODEL_LOADED = False
    ERROR_MSG = str(e)


def process_document(image_path):
    if image_path is None:
        return pd.DataFrame(), "Файл не выбран"

    if not MODEL_LOADED:
        return pd.DataFrame(), f"Ошибка загрузки модели: {ERROR_MSG}"

    try:
        img = cv2.imread(image_path)
        if img is None:
            return pd.DataFrame(), "Ошибка чтения изображения"

        res = reader.process(img)

        if not res or not getattr(res, 'documents', None):
            return pd.DataFrame(), "Документ не распознан"

        parsed_data = []
        log_text = ""

        for doc in res.documents:
            # Если есть поля - добавляем в таблицу
            if hasattr(doc, 'fields') and isinstance(doc.fields, dict):
                for key, value in doc.fields.items():
                    parsed_data.append({"Поле": key, "Значение": str(value)})
            else:
                log_text += str(doc) + "\n"

        if parsed_data:
            df = pd.DataFrame(parsed_data)
            status = "Успешно"
        else:
            df = pd.DataFrame(columns=["Поле", "Значение"])
            status = log_text if log_text else "Данные не найдены"

        return df, status

    except Exception as e:
        return pd.DataFrame(), f"Ошибка: {str(e)}"


# ==========================================
# ИНТЕРФЕЙС (Только функционал, без текста)
# ==========================================
with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            image_input = gr.Image(sources=['upload'], type="filepath", label="Документ")
            submit_btn = gr.Button("Распознать")

        with gr.Column():
            table_output = gr.Dataframe(label="Извлеченные данные", headers=["Поле", "Значение"], interactive=False)
            status_output = gr.Textbox(label="Статус", interactive=False, lines=1)

    submit_btn.click(
        fn=process_document,
        inputs=image_input,
        outputs=[table_output, status_output]
    )

if __name__ == "__main__":
    demo.launch()
