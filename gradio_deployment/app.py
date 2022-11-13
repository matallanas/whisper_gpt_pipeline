import gradio as gr
import tensorflow as tf
import datasets
from notebooks.starter_model_training import tokenize_function, create_dataset, compile_model, gen_text
'''
We want to create an application that allows the user to select a dataset from a specified list
and pass that with specified parameters to a model to train it on.

Then, we want a way to allow the user to select hyperparameters for their model, train it, and then 
Generate some text! 

'''

MODEL = ""

def train_model(dat, epochs, model_checkpoint):
    # trains model given parameters

    model = compile_model(model_checkpoint=model_checkpoint)

    ds = create_dataset(dat)
    tok_data = tokenize_function(ds, model_checkpoint)

    mod_history = model.fit(tok_data, epochs = epochs)
    MODEl = model

    return model




# App Construction



demo = gr.Blocks()

with demo:
    gr.Markdown("<h1><center>Generate Text from Youtube with Whisper and GPT!</center></h1>")
    #dataset selector
    with gr.Row():
        with gr.Column():
            ds = gr.Dropdown(["Whispering-GPT/whisper-transcripts-the-verge"], value = "Whispering-GPT/whisper-transcripts-the-verge")
            #model parameters
            
            epochs = gr.Slider(minimum = 1, maximum = 10, value  = 1, step = 1, interactive = True)
           #block_size = gr.Dropdown([32, 64, 128, 256], value = 64)
            model_checkpoint = gr.Dropdown(["distilgpt2"], value = "distilgpt2")
        with gr.Column():
             #train button
            begin_training = gr.Button("Begin Training!")
            #button to generate text iff training done
            seed_text = gr.Textbox("Write some seed text here")
            create_text = gr.Button("Generate some text!")
    with gr.Row():
        text_output = gr.Textbox(value = "Generated text will appear here")
        create_text.click(gen_text, inputs = [model_checkpoint, MODEL, seed_text, 3], outputs=[text_output])

    
    begin_training.click(train_model, inputs = [ds, model_checkpoint, epochs])


demo.launch()

