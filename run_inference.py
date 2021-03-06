from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import re
import math
import os
import inference_utils.vocabulary as vocabulary
import time
import tensorflow as tf
import json
import configuration

import inference_utils.caption_generator as caption_generator
import inference_wrapper

FLAGS = tf.flags.FLAGS

tf.flags.DEFINE_string("checkpoint_path", "/home/g1201umer/im2txt/model/train",
                       "Model checkpoint file or directory containing a "
                       "model checkpoint file.")
tf.flags.DEFINE_string("vocab_file", "/home/g1201umer/im2txt/data/mscoco/word_counts.txt", "Text file containing the vocabulary.")
tf.flags.DEFINE_string("input_files", "",
                       "File pattern or comma-separated list of file patterns "
                       "of image files.")
def run_inference(file1):
  # Build the inference graph.
  g = tf.Graph()
  with g.as_default():
    model = inference_wrapper.InferenceWrapper()
    restore_fn = model.build_graph_from_config(configuration.ModelConfig(),
                                               FLAGS.checkpoint_path)
  g.finalize()

  # Create the vocabulary.
  vocab = vocabulary.Vocabulary(FLAGS.vocab_file)

  filenames = []
  for file_pattern in FLAGS.input_files.split(","):
    filenames.extend(tf.gfile.Glob(file_pattern))
  tf.logging.info("Running caption generation on %d files matching %s",
                  len(filenames), FLAGS.input_files)

  with tf.Session(graph=g) as sess:
    # Load the model from checkpoint.
    restore_fn(sess)
    filename="/home/g1201umer/myproject/images/"+file1
    # Prepare the caption generator. Here we are implicitly using the default
    # beam search parameters. See caption_generator.py for a description of the
    # available beam search parameters.
    generator = caption_generator.CaptionGenerator(model, vocab)

    #for filename in filenames:
    with tf.gfile.GFile(filename, "r") as f:
      image = f.read()
    captions = generator.beam_search(sess, image)
    print("Captions for image %s:" % os.path.basename(filename))
    #for i, caption in enumerate(captions):
      # Ignore begin and end words.
    sentence = [vocab.id_to_word(w) for w in captions[0].sentence[1:-1]]
    sentence = " ".join(sentence)
    print("  %s " % (sentence))
  return sentence

if __name__ == "__main__":
  tf.app.run()
