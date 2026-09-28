# Next steps

1. Extract this archive. Review PROJECT.md and AGENTS.md to confirm the role boundaries.
2. Create a private GitHub repository with a name of your choosing. Add the contents of election-model-starter/ at the repository root, including .gitignore and the directory marker files. Make the initial commit.
3. Connect Codex and Claude Code to the repository through their respective setups. Do not send credentials in chat. Share the repository URL in this conversation after access is ready.
4. Ask each coding tool to read PROJECT.md, STATUS.md, and its instruction file and summarize the boundaries before editing. Use one tool at a time initially.
5. Work with Claude to fill CLAUDE.md with your preferred tutoring and review workflow. Keep methodology blank until you make actual model decisions.
6. Choose the first forecast scope: Senate races, House outcomes, or another explicit target. Then choose one tractable first unit of analysis and a minimum deliverable. Record these in PROJECT.md.
7. Tell ChatGPT your local operating system, editor, Python setup (if any), available weekly time, and data budget. Use these to configure a minimal environment; no versions or dependencies have been assumed here.
8. Ask ChatGPT to assess candidate sources for the chosen scope and propose a data schema. Record approved choices in docs/data_sources.md and docs/data_dictionary.md. Implement collection and mechanical cleaning only after those choices are clear.
9. Discuss the baseline mathematics with Claude, record approved assumptions in docs/methodology.md, and write your own first model.
10. Use docs/handoff_template.md when switching assistants. Transfer conclusions into repository files rather than relying on either assistant's private chat memory.

## First GitHub tasks to create after connection

- Confirm scope and minimum deliverable — Rahan.
- Define Claude tutoring and review instructions — Rahan with Claude.
- Configure Python environment and reproducible setup — Codex, after environment details are known.
- Verify poll sources and propose input schema — ChatGPT/Codex, after scope is chosen.
- Define baseline and evaluation approach — Rahan with Claude.

These are proposed tasks; no GitHub issues, integrations, or workflows have been created.
