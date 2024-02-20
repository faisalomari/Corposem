# Corposem
  <h1>Hebrew NLP Corposem</h1>
  <p>This repository contains the implementation of an assignment for a Natural Language Processing (NLP) course at the University of Haifa. The assignment is written in Hebrew and involves processing textual data from Israeli parliamentary protocols.</p>
  <h2>Assignment Overview</h2>
  <p>The assignment involves two main stages:</p>
  <ol>
    <li><strong>Text Processing</strong>: Extracting relevant data from parliamentary protocols, including identifying speakers and their corresponding speeches.</li>
    <li><strong>Zipf's Law Implementation</strong>: Analyzing the cleaned text corpus to check if Zipf's Law holds true for the dataset.</li>
  </ol>
  <h2>How to Run</h2>
  <h3>Prerequisites</h3>
  <ul>
    <li>Python <3.7 installed on your system.</li>
    <li>Required Python packages installed. You can install them using <code>pip install -r requirements.txt</code>.</li>
  </ul>
  <h3>Steps to Run</h3>
  <ol>
    <li><strong>Text Processing</strong>:
      <ul>
        <li>Execute the script <code>processing_knesset_corpus.py</code> with the input corpus directory path and output CSV file path as arguments:</li>
        <pre><code>python processing_knesset_corpus.py &lt;input_corpus_dir&gt; &lt;output_csv_path&gt;</code></pre>
      </ul>
    </li>
    <li><strong>Zipf's Law Implementation</strong>:
      <ul>
        <li>Execute the script <code>knesset_zipf_law.py</code> with the input CSV file path and output plot image file path as arguments:</li>
        <pre><code>python knesset_zipf_law.py &lt;input_csv_file&gt; &lt;output_plot_path&gt;</code></pre>
      </ul>
    </li>
  </ol>
  <h3>Example</h3>
  <pre><code>python processing_knesset_corpus.py input_data/ output_data/knesset_corpus.csv
python knesset_zipf_law.py output_data/knesset_corpus.csv output_data/zipf_law_plot.png</code></pre>
<footer>
    <p>For any issues or inquiries, please contact Faisal Omari - <a href="mailto:faisalomari321@gmail.com">faisalomari321@gmail.com</a></p>
</footer>

