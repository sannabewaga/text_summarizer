from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from transformers import TrainingArguments, Trainer
from transformers import DataCollatorForSeq2Seq
import torch
from datasets import load_from_disk
import os
from src.textSummarizer.entity import ModelTrainerConfig
from src.textSummarizer.logging import logger

class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config
        logger.info("Initialized ModelTrainer with config: %s", self.config)

    def train(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {device}")

        logger.info("Loading tokenizer and model from checkpoint: %s", self.config.model_ckpt)
        tokenizer = AutoTokenizer.from_pretrained(self.config.model_ckpt)
        model_pegasus = AutoModelForSeq2SeqLM.from_pretrained(self.config.model_ckpt).to(device)

        logger.info("Creating data collator...")
        seq2seq_data_collator = DataCollatorForSeq2Seq(tokenizer, model=model_pegasus)

        logger.info("Loading dataset from: %s", self.config.data_path)
        dataset_samsum_pt = load_from_disk(self.config.data_path)

        logger.info("Preparing training arguments...")
        trainer_args = TrainingArguments(
            output_dir=self.config.root_dir,
            num_train_epochs=self.config.num_train_epochs,
            warmup_steps=self.config.warmup_steps,
            per_device_train_batch_size=self.config.per_device_train_batch_size,
            per_device_eval_batch_size=self.config.per_device_train_batch_size,  # reuse
            weight_decay=self.config.weight_decay,
            logging_steps=self.config.logging_steps,

            eval_steps=self.config.eval_steps,
            save_steps=self.config.save_steps,
            gradient_accumulation_steps=self.config.gradient_accumulation_steps
        )


        logger.info("Initializing Trainer...")
        trainer = Trainer(
            model=model_pegasus,
            args=trainer_args,
            tokenizer=tokenizer,
            data_collator=seq2seq_data_collator,
            train_dataset=dataset_samsum_pt["test"],
            eval_dataset=dataset_samsum_pt["validation"]
        )

        logger.info("Starting training...")
        trainer.train()
        logger.info("Training completed successfully.")

        model_dir = os.path.join(self.config.root_dir, "pegasus-samsum-model")
        tokenizer_dir = os.path.join(self.config.root_dir, "tokenizer")

        logger.info("Saving model to: %s", model_dir)
        model_pegasus.save_pretrained(model_dir)

        logger.info("Saving tokenizer to: %s", tokenizer_dir)
        tokenizer.save_pretrained(tokenizer_dir)

        logger.info("Model and tokenizer saved successfully.")

    def run(self):
        self.train()
