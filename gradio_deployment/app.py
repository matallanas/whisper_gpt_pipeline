import gradio as gr
from notebooks.starter_model_training import create_dataset, compile_model, gen_text
from transformers import DefaultDataCollator
'''
We want to create an application that allows the user to select a dataset from a specified list
and pass that with specified parameters to a model to train it on.

Then, we want a way to allow the user to select hyperparameters for their model, train it, and then 
Generate some text! 

'''

MODEL = ""

def train_model(dat, model_checkpoint, epochs):
    # trains model given parameters

    model = compile_model(model_checkpoint=model_checkpoint)

    ds = create_dataset(dat, model_checkpoint=model_checkpoint)

    data_collator = DefaultDataCollator(return_tensors="tf")

    train_set = ds["train"].to_tf_dataset(
        columns=["attention_mask", "input_ids", "labels"],
        shuffle=True,
        batch_size=16,
        collate_fn=data_collator,
    )

    mod_history = model.fit(train_set, epochs = epochs)
    MODEl = model

    return model

def generate_text(model_checkpoint, seed_text):

    output = gen_text(model_checkpoint=model_checkpoint, model=MODEL, seed_text=seed_text)
    return output


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
            model_checkpoint = gr.Dropdown(["distilgpt2"], value = "distilgpt2", type = "value")
        with gr.Column():
             #train button
            begin_training = gr.Button("Begin Training!")
            #button to generate text iff training done
            seed_text = gr.Textbox("Write some seed text here")
            create_text = gr.Button("Generate some text!")
    with gr.Row():
        text_output = gr.Textbox(value = "Generated text will appear here")
        create_text.click(generate_text, inputs = [model_checkpoint, seed_text], outputs=[text_output])

    
    begin_training.click(train_model, inputs = [ds, model_checkpoint, epochs])


demo.launch()

