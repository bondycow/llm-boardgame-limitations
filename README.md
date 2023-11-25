# **Evaluating the Limitations of Large Language Models in Board Games**

## Abstract
In recent years, advancements in Large Language Models (LLMs) have led to significant interests in the models’ capabilities in different areas. This paper investigates their deficiency in their board game performance, using games such as Chess, Connect 4, and Tic Tac Toe. Key findings from the experiments include inconsistencies in board representation in Tic Tac Toe, Connect 4, and Chess. Furthermore, GPT-4's chess puzzle-solving ability is tested across different difficulty levels and prompting strategies. For easy puzzles, GPT-4 achieved an accuracy of 19.8% with zero-shot prompting, which improved to 30% with one-shot prompting and 32.8% with two-shot prompting. In intermediate puzzles, the accuracies are 14%, 17.6%, and 18.6% for zero-shot, one-shot, and two-shot prompting, respectively. For hard puzzles, the accuracies are 9.80%, 13.5%, and 15% for the same prompting strategies. Given the same puzzles but in multiple choice formats, the three test sets yield much improved accuracies of 48.2%, 49.4%, and 47.2%, respectively. Additionally, when given repeated attempts at easy puzzles, GPT-4's accuracy improved from 19.8% to 33.4%. These results highlight the key challenges faced by LLMs in playing board games, offering potential areas for the current models to improve. At the same time, the discussions provide insights on their inability to perform other general tasks regarding memory storage, and thinking processes that are not just limited to board games.

Full paper can be found here: [temporary location/format awaiting publish](https://docs.google.com/document/d/1vDg2jCfhzXHS7l3EuRCBAL-sL5MGFfxjAT0SDJFP5bE/edit#heading=h.r9pu5qsdfoed](https://drive.google.com/file/d/1dmfoSWFURRXzKTbYHqDs4T7bLCA4AqQg/view?usp=sharing)

## Mechanism
The study aims to examine multiple factors that can potentially cause the limitation of LLM performance in board games, including board state interpretation, and strategic reasoning. Specific experiments are designed to probe each factor, and the full experiment detail can be found in the paper. 

### Board State Interpretation
For an LLM to perform effectively, it must be able to accurately interpret the board game’s state at any given moment during the game. Given that LLMs are inherently stateless, their ability to recall such information across the span of a long conversation comes into question, though, through the usage of information tokenization, language models are able to recall the previous queries based on the tokened information stored. An alternative attempt to ensure the model is accurately remembering the board state is to supply the current game state on each turn, either using an ASCII coded notation, or using a specialized notation in board game, such as FEN (Forsyth–Edwards Notation) in chess. Understanding how well an LLM can interpret, remember, and utilize board state information is critical for evaluating its limitations in board games.  Experiments are designed to probe each aspect accordingly.
### Strategic Reasoning
While the ability to correctly interpret a board state is crucial, the actual gameplay, given the model can accurately recall the board state, offers more insight into complex decision making and logical reasoning. Humans often engage in both sequential and parallel thinking, weighing multiple options simultaneously and considering the implications of each move several turns ahead. In contrast, LLMs are primarily designed for text completion tasks and operate in a more sequential manner, considering one piece of information at a time. Thus, their performance may be affected by this thought process. Consequently, prompting strategy may be a pivotal factor affecting models’ performance in board games. By manipulating the prompt, the user can stimulate the model to think in a certain way, potentially optimizing the model’s performance. In both of the sections, experiments are done based on an open-source comprehensive chess puzzle database. To utilize it in the experiment, the data is adjusted and normalized. Understanding the limitations and capabilities of LLMs in strategic reasoning is therefore pivotal to assess their suitability for board games. 

## Dataset
All puzzles are downloaded from open-source Lichess database, and all of the processing code/resulting dataset can be found in folders under the project. [lichess.org open database](https://database.lichess.org/#puzzles)

## Results
The link to the stateless interaction testing chat is linked here: [ChatGPT](https://chat.openai.com/share/c731c20e-2a28-41a3-9bca-1f0d9e5609ce)
All the other data tables can be found under the project folder.



## IMPORTANT: Enhancements
GPT-3.5 instruct is shown to have improved performance in board games. This study lacks experimentation with the model, so more testing can be done using the same mechanism on that model for more experimentations. 
