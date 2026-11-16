# Nitro XML enhancement proposals

Live site: https://jgridifier.github.io/nitro-xml-proposals/

- All content comes from `proposals.json`. To add a proposal, append an entry (images in `img/`) and run `python3 build.py`, which regenerates `index.html` and `p/<id>.html`.
- Each proposal links to one issue in `jgridifier/nitro-xml` labelled `proposal`. 👍 on the issue approves it, 👎 declines it. `status.js` refreshes the badges from the live issue (labels `approved` / `building`, closed = shipped).
- Images labelled MOCKUP are DOM-overlay mockups rendered on the real demo with Playwright; "today" images are unmodified screenshots of the demo at that day's `main`.
