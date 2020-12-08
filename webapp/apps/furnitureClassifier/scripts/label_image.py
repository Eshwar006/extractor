# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import time
from pathlib import Path

import numpy as np
import tensorflow as tf
tf.compat.v1.disable_eager_execution()

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class LabelImage(object):

  model_file = "/furnitureClassifier/tf_files/retrained_graph.pb"
  label_file = "/furnitureClassifier/tf_files/retrained_labels.txt"

  def load_graph(self):
    # /Users/eshwar/Desktop/hackathon/extractor/out/production/messaging_platform/auth
    model_file = str(Path(__file__).resolve().parent.parent.parent) + self.model_file
    graph = tf.Graph()
    graph_def = tf.compat.v1.GraphDef()

    with open(model_file, "rb") as f:
      graph_def.ParseFromString(f.read())
    with graph.as_default():
      tf.import_graph_def(graph_def)

    return graph

  def load_labels(self):
    label_file = str(Path(__file__).resolve().parent.parent.parent) + self.label_file
    label = []
    proto_as_ascii_lines = tf.io.gfile.GFile(label_file).readlines()
    for l in proto_as_ascii_lines:
      label.append(l.rstrip())
    return label

  def read_tensor_from_image_file(self, file_name, input_height=299, input_width=299,
                                  input_mean=0, input_std=255):
    file_name = str(Path(__file__).resolve().parent.parent.parent) + file_name
    input_name = "file_reader"
    output_name = "normalized"
    file_reader = tf.io.read_file(file_name, input_name)
    if file_name.endswith(".png"):
      image_reader = tf.image.decode_png(file_reader, channels = 3,
                                         name='png_reader')
    elif file_name.endswith(".gif"):
      image_reader = tf.squeeze(tf.image.decode_gif(file_reader,
                                                    name='gif_reader'))
    elif file_name.endswith(".bmp"):
      image_reader = tf.image.decode_bmp(file_reader, name='bmp_reader')
    else:
      image_reader = tf.image.decode_jpeg(file_reader, channels = 3,
                                          name='jpeg_reader')
    float_caster = tf.cast(image_reader, tf.float32)
    dims_expander = tf.expand_dims(float_caster, 0);
    resized = tf.image.resize(dims_expander, [input_height, input_width])
    normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
    sess = tf.compat.v1.Session()
    # print(sess.run(normalized))
    result = sess.run(normalized)

    return result

  def label(self, file_name="tf_files/flower_photos/daisy/3475870145_685a19116d.jpg"):
    input_height = 224
    input_width = 224
    input_mean = 128
    input_std = 128
    input_layer = "input"
    output_layer = "final_result"

    graph = self.load_graph()
    t = self.read_tensor_from_image_file(file_name,
                                    input_height=input_height,
                                    input_width=input_width,
                                    input_mean=input_mean,
                                    input_std=input_std)

    input_name = "import/" + input_layer
    output_name = "import/" + output_layer
    input_operation = graph.get_operation_by_name(input_name);
    output_operation = graph.get_operation_by_name(output_name);

    with tf.compat.v1.Session(graph=graph) as sess:
      start = time.time()
      results = sess.run(output_operation.outputs[0],
                        {input_operation.outputs[0]: t})
      end=time.time()
    results = np.squeeze(results)

    top_k = results.argsort()[-5:][::-1]
    labels = self.load_labels()

    print('\nEvaluation time (1-image): {:.3f}s\n'.format(end-start))
    # template = "{} (score={:0.5f})"
    result = []
    for i in top_k:
      # print(template.format(labels[i], results[i]))
      result.append({"name": labels[i], "score": results[i]})
    return result
