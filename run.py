import gradio as gr
import cv2

try:
    from docreader import DocReader

    reader = DocReader()
    MODEL_LOADED = True
except Exception as e:
    MODEL_LOADED = False
    ERROR_MSG = str(e)


def f(im):
    if im is None:
        return {"error": "Файл не выбран"}

    if not MODEL_LOADED:
        return {"error": f"Ошибка: {ERROR_MSG}"}

    try:
        img = cv2.imread(im)
        if img is None:
            return {"error": "Ошибка чтения изображения"}

        res = reader.process(img)

        if not res or not getattr(res, 'documents', None):
            return {"error": "Документ не распознан"}

        output_json = {"document": []}

        for doc in res.documents:
            doc_name = getattr(doc, 'doc_type', 'unknown')
            zones_list = []

            if hasattr(doc, 'fields') and isinstance(doc.fields, dict):
                for key, value in doc.fields.items():
                    zones_list.append({key: value})
            else:
                zones_list.append({"raw_data": str(doc)})

            output_json["document"].append({
                "doc_name": doc_name,
                "zones": zones_list
            })

        return output_json

    except Exception as e:
        return {"error": str(e)}


with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            im = gr.Image(sources=['upload'], type="filepath", label="Документ")
            btn = gr.Button("Распознать")

        with gr.Column():
            out = gr.JSON(label="Результат")

    btn.click(fn=f, inputs=im, outputs=out)

if __name__ == "__main__":
    demo.launch()
