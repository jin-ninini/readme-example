Please refactor and organize the current project according to the following requirements.

Do not change the core behavior of the existing project unless necessary for the refactoring.

# 1. Project Structure

Organize the repository with the following top-level structure as the default:

project/
├── data/
├── src/
├── models/
├── requirements.txt
├── README.md
├── train.py
├── valid.py
└── test.py

Additional top-level execution scripts may be added only when they represent an independent workflow that should be executed directly.

For example:

├── crawling.py

If crawling is a standalone process, it should be implemented as `crawling.py` at the project root rather than being placed inside `src/`.

Note:
- Use `valid.py` as the validation entry point.
- If the existing project already uses `vaild.py` intentionally, verify the references and rename them consistently to `valid.py` if there is no compatibility reason to keep the typo.


# 2. Entry Point Design

Top-level Python files should act as execution entry points.

Examples:

- `train.py`      → model training
- `valid.py`      → model validation
- `test.py`       → model testing / evaluation
- `crawling.py`   → data crawling, if crawling is required

These files should contain only the high-level execution flow.

Do NOT implement large amounts of business logic, preprocessing logic, model logic, or utility functions directly inside these files.

Prefer the following pattern:

1. Import reusable functions/classes from `src/`
2. Load configuration or arguments
3. Execute the workflow
4. Save or display the result

Use:

if __name__ == "__main__":
    main()

for executable scripts whenever appropriate.


# 3. src/ Structure

Move reusable implementation logic into `src/`.

Split modules based on clear functional responsibilities.

Use descriptive filenames that immediately communicate their purpose.

For example, depending on what exists in the current project:

src/
├── data_loader.py
├── preprocessing.py
├── model.py
├── trainer.py
├── evaluator.py
├── inference.py
├── utils.py
└── config.py

Do NOT create these files blindly.

First inspect the existing codebase and determine the actual responsibilities in the project, then create only the modules that are necessary.

File names should clearly represent their responsibilities.


# 4. Code Reusability

Avoid duplicated code.

If training, validation, and testing use the same functionality, extract that functionality into `src/` and reuse it.

Examples of reusable functionality include:

- dataset loading
- preprocessing
- feature engineering
- model initialization
- checkpoint loading
- inference
- evaluation metrics
- configuration loading
- path handling
- logging
- common utility functions

For example, `train.py`, `valid.py`, and `test.py` should NOT contain separate copies of the same dataset-loading or preprocessing implementation.

Instead, they should import the same reusable implementation from `src/`.


# 5. Separation of Responsibilities

Keep each module focused on one clear responsibility.

Preferred:

src/data_loader.py
→ dataset loading

src/preprocessing.py
→ preprocessing and transformation

src/model.py
→ model definition / model loading

src/trainer.py
→ training-related functions

src/evaluator.py
→ validation and evaluation

Avoid ambiguous files containing unrelated logic.

Also avoid generic filenames such as:

- `common.py`
- `functions.py`
- `helper.py`
- `code.py`

unless there is a strong reason to use them.

Names should explain what the module actually does.


# 6. data/

Use `data/` for project datasets and intermediate data artifacts.

If necessary, organize it further based on the existing project, for example:

data/
├── raw/
├── processed/
└── output/

Do not introduce unnecessary subdirectories if the project does not need them.

Large datasets or generated files that should not be committed must be handled appropriately through `.gitignore`.


# 7. models/

Use `models/` for model-related artifacts such as:

- trained model files
- checkpoints
- weights
- serialized models

Do not store Python source code in `models/`.

Model implementation code should be located under `src/`.


# 8. requirements.txt

Review the existing source code and update `requirements.txt`.

Requirements:

- Include packages actually required to run the project.
- Remove dependencies that are clearly unused.
- Make sure a clean environment can install the dependencies required by the project.
- Do not add packages merely because they might be useful.


# 9. README.md

Rewrite `README.md` in English.

Use the following repository as the primary style/reference:

https://github.com/jin-ninini/readme-example

Inspect that repository before writing the README and follow its overall presentation style, structure, formatting, and level of detail where applicable.

However, the README content must describe THIS project accurately. Do not copy irrelevant content from the reference repository.

At minimum, README.md should make the following immediately understandable:

1. Project name
2. Project overview
3. Objective / purpose
4. Project structure
5. Environment setup / installation
6. Dataset or data preparation
7. How to run the project
8. Training
9. Validation
10. Testing
11. Crawling, if applicable
12. Model / output location
13. Dependencies / requirements

Include a clear project tree similar to:

project/
├── data/
├── src/
├── models/
├── requirements.txt
├── README.md
├── train.py
├── valid.py
├── test.py
└── crawling.py        # only if required

For execution instructions, provide actual commands supported by the project, such as:

python train.py
python valid.py
python test.py
python crawling.py

Do not document commands, arguments, features, or dependencies that are not actually implemented.


# 10. Refactoring Rules

Before modifying the project:

1. Inspect the entire existing codebase.
2. Identify each file's responsibility.
3. Identify duplicated implementations.
4. Identify code that should become reusable `src/` modules.
5. Identify standalone workflows that should become root-level executable scripts.

Then perform the refactoring.

Important constraints:

- Preserve existing functionality.
- Avoid unnecessary rewrites.
- Avoid over-engineering.
- Do not introduce unnecessary abstractions.
- Do not create modules merely to make the directory look organized.
- Prefer simple, readable Python.
- Remove duplication where practical.
- Update imports after moving code.
- Update paths after reorganizing files.
- Make sure functions have clear responsibilities and names.


# 11. Validation After Refactoring

After restructuring the project:

1. Check all Python imports.
2. Check file and directory paths.
3. Check references to moved files.
4. Check `requirements.txt`.
5. Verify that each entry point can be executed independently where applicable.
6. Check that training, validation, testing, and crawling still use the intended common modules.
7. Make sure README commands match the actual implementation.
8. Remove obsolete files left behind by the refactoring.
9. Do not leave duplicated legacy implementations in the repository.

Finally, show the resulting directory tree and briefly summarize:

- what was moved
- what was refactored
- what reusable modules were created
- what duplication was removed
- whether any behavior was intentionally changed
