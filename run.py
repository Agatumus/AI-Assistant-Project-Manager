import gradio as gr

# def processing(image):
#     # model connection
#     # pred = model(image)
#     return pred

def f(im):
    if im is None: return "Ошибка: файл не выбран"
    # simulation
    # k = 0
    return "Документ успешно загружен. Тип: Паспорт РФ. Данные отправлены в обработку."

with gr.Blocks() as demo:
    # header
    gr.Markdown("# AI Assistant Demo")
    
    with gr.Row():
        # input
        im = gr.Image(sources=['upload'], type="filepath", label="Входной документ")
        # output log
        out = gr.Textbox(label="Системный лог", interactive=False)
    
    # controls
    btn = gr.Button("Загрузить и обработать", variant="primary")
    
    # events
    btn.click(f, inputs=im, outputs=out)

demo.launch()