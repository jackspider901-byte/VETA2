# VEXA / Luxury streetwear UI & UX

**A responsive, interactive design prototype with editable source and a developer handoff.**

## Start here

Open **VEXA-Prototype.html** in a desktop browser. It is a single, self-contained file with its code and images embedded. No build step, npm installation, external font service or image connection is required to view it. A file preview inside a messaging app may not run JavaScript; open the saved file in a browser instead.

Open **preview/index.html** for the screen-review gallery. Read **VEXA-UIUX-Handoff.pdf** for the design decisions, behavioural specification and delivery limitations.

For the complete checkout demonstration, follow the **Demo only · Explore the handoff** link at the top of the prototype, choose **Load a sample bag**, continue to checkout and select **Use sample details**. The final step lets you simulate either a successful or a declined payment. No real card details are requested.

## What is included

| File or folder | Purpose |
| --- | --- |
| `VEXA-Prototype.html` | Portable interactive prototype, including embedded assets. |
| `index.html` | Editable entry point using the separate source files. |
| `src/styles.css` | Visual tokens, responsive layouts and reusable component styling. |
| `src/catalogue.js` | Eight fictional products, sample stock, prices, sizing and colours. |
| `src/app.js` | Routing, search, filters, product options, bag and simulated checkout. |
| `design/screens/` | 22 editable SVG screen snapshots, covering desktop and mobile. |
| `design/tokens.json` | Machine-readable visual tokens. |
| `design/screen-manifest.json` | Index of every exported screen and its reference width. |
| `preview/` | 39 PNG exports plus the navigable screen-review gallery. |
| `assets/` | Local concept imagery and editable wordmark/favicon SVGs. |
| `docs/HANDOFF.md` | Editable written design and implementation handoff. |
| `docs/qa-results.json` | Results and scope of the 61 automated browser checks. |
| `tests/test_prototype.py` | Repeatable interaction checks. |
| `build.py` | Rebuild the portable HTML after modifying the source. |
| `serve.py` | Optional local server using Python's standard library. |
| `tools/` | Screen/SVG export and PDF handoff generation tools. |

## Scope

The connected journey covers home, collection, search suggestions, sorting and filters, product detail, colour and size selection, a sample size guide, bag drawer, full bag, guest details, delivery selection, payment simulation and confirmation. Also included: About, editorial lookbook, unavailable product, empty bag, no results, mobile navigation, supporting-policy placeholders and the live component/design-system page.

The interface includes loading, selected, disabled, invalid, success and empty states. Product-gallery swipes are supported on touch screens. Core navigation does not rely on hover.

## Editing the design

Change the catalogue and all illustrative product values in `src/catalogue.js`. Prices are GBP amounts stored in integer minor units: `16000` means £160. Changing the currency setting does **not** convert prices. Change the amount fixtures as well.

Update colours, spacing, type and breakpoints in `src/styles.css`. The JSON tokens document the same system but are not a live code-generation source. Keep the CSS and JSON in sync after changing tokens.

Edit screen templates, interface copy and interactions in `src/app.js`. Replace images in `assets/` using the same filenames, or update the image references in the catalogue. Each product colourway names its own image file.

After editing, run:

```sh
python3 build.py
```

The generated `VEXA-Prototype.html` is rebuilt from the separate source. Do not edit only the generated file unless you intend to discard those edits on the next build.

## Running locally or on a static host

For a local HTTP origin, run:

```sh
python3 serve.py
```

Open the address printed in the terminal. To change the port, use `python3 serve.py --port 8080`.

The editable site is static HTML/CSS/JavaScript. Publish `index.html`, `src/` and `assets/` together to a static host, or publish the standalone `VEXA-Prototype.html` renamed to `index.html`. There is no PHP, database or build output directory. Hash-based routes do not require server-side route rewrites. Deployment itself has not been performed or tested in this delivery.

Browser storage behaviour for local `file:` pages is not standardised consistently. The bag uses local storage where it is available and falls back to the current page session otherwise. An HTTP origin is the preferred way to check persistence. Checkout details are intentionally held in memory, not local storage. See the MDN reference in the handoff.

## Using the editable screen exports

The SVGs contain editable text fragments, shapes and nested groups; product photography remains raster. They can be opened in an SVG-capable vector editor. **They are not native Figma files and do not include Figma Auto Layout, component variants or prototype wires.** Font substitution and image blending may vary between editors. The HTML/CSS prototype is the reference for responsive behaviour and final browser rendering.

The PNGs are static review snapshots. Use the live prototype, not a PNG, to evaluate interactions.

## Testing and regeneration

Runtime dependencies: none beyond a browser with JavaScript enabled.

Optional development dependencies:

```sh
python3 -m pip install -r requirements-dev.txt
python3 -m playwright install chromium
python3 tests/test_prototype.py
python3 tools/export_screens.py
python3 tools/build_handoff.py
```

The delivered QA run passed **61 checks** in Chromium using the portable file injected locally into a browser page. It covered the main purchase simulation, invalid size/email cases, filter recovery, colour changes, quantities, declined-payment recovery, selected responsive widths, focus return, reduced motion and local-storage validation fixtures. Storage fixtures are mocked, not a certification of cross-session persistence.

Safari, Firefox, real mobile hardware, screen-reader use, production performance, user research and live commerce integrations have not been validated. The handoff explicitly distinguishes implementation from certification.

## Production boundary

VEXA is a **working brand name**, not a trademark-cleared identity. This is a design prototype, not a functioning retail business. Products, inventory, measurements, prices, taxes, shipping rates and receipts are illustrative. No live sign-in, subscriptions, payment gateway, order fulfilment, customer support inbox or email delivery is connected.

All imagery comes from the earlier generated VEXA concept in this conversation. The original contains small product images; upscaling does not create real detail. Detail-gallery views are crops, not additional photographs. Chalk colourways are illustrative recolourings. Replace these assets, product specifications and policy placeholders with approved real content before launch.

No customer research has been invented. Usability assumptions still need testing with actual shoppers.
