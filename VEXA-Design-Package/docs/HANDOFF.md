# VEXA / Design handoff 01

**Version:** 1.0 · **Date:** 16 September 2026  
**Deliverable:** Responsive front-end design prototype, editable code, SVG screen exports and documented UI system.  
**Reference layouts:** 1440px desktop and 390px mobile.  
**Working market/currency:** Illustrative GBP prices, retained from the initial concept. This is not a confirmed commercial market decision.

## 1. Brief and design hypothesis

Create a premium streetwear shopping experience with an editorial identity and a straightforward purchase journey. VEXA is a temporary brand identity for this exercise. The design assumes a unisex collection of heavyweight essentials, statement outerwear, trousers and accessories.

The visual direction is deliberate rather than decorative: warm paper, near-black, one restrained brick-red action colour, large campaign typography and clean product presentation. Editorial asymmetry is used on campaign and brand pages. Product browsing, options, basket and checkout use familiar, predictable layouts.

The hypothesis is that the intended audience should be able to understand the brand, evaluate garment form and fit, and reach checkout without unnecessary steps. This is a design hypothesis, not the result of customer research. No interviews, usability results, customer testimonials or commercial performance claims have been invented.

## 2. Information architecture and primary journey

Primary navigation: Shop, New arrivals, Collections and About. Search, account information and the shopping bag are separate utilities. Mobile replaces the navigation links with a drawer while keeping search and bag available.

Primary journey:

`Homepage > Collection > Product > Select colour and size > Add to bag > Review bag > Guest details > Delivery > Payment simulation > Confirmation`

Secondary routes: editorial lookbook, brand story, live design system, prototype guide, sizing and supporting policy placeholders. Search is a modal with live suggestions; a full search submits into the collection route with a query parameter.

The account control explains the guest-only scope. It does not pretend that sign-in or account management is connected. No invented social accounts or support contacts are provided.

## 3. Screen coverage

The delivery contains 39 desktop/mobile PNG exports and 22 editable SVG screen snapshots. Core SVG layouts include homepage, collection, product, bag, the three checkout stages, confirmation, About, lookbook and design system at both reference widths. Additional PNGs capture no results, empty bag, unavailable product, search, filters, size guide, bag drawer, mobile navigation and the declined-payment state.

The live prototype is the behavioural reference. PNGs are static snapshots. SVGs preserve editable text fragments, shapes and groups, with raster photographs. They are not native Figma files, Auto Layout frames, component variants or wired Figma prototypes. Import appearance may vary by editor; use HTML/CSS and the PNGs to resolve visual differences.

## 4. Visual system

| Token | Value | Use |
| --- | --- | --- |
| Paper | `#F4F2ED` | Main page background and light text on dark sections. |
| Surface | `#E9E6DF` | Product photography fields and order summaries. |
| Ink | `#171715` | Main text, navigation, primary neutral controls. |
| Muted | `#66655E` | Supporting information and utility labels. |
| Accent | `#B63823` | Campaign CTA, purchase action and focus outlines. |
| Rule | `#CFCBC2` | Quiet dividers and secondary boundaries. |
| Success | `#276341` | Demo success feedback. |
| Error | `#A52424` | Validation and payment-recovery messages. |

Typography uses system Arial/Helvetica for display and interface copy, with Courier New for small utility labels. No font files or external font requests are included. Large display type uses tight tracking; paragraphs use comfortable line heights. Essential field input text becomes 16px on narrow layouts. Utility labels are not used as a substitute for readable product information.

The spacing scale uses 4, 8, 12, 16, 20, 24, 28, 32, 40, 48, 64, 76 and 80px. Reference page margins are 48px desktop and 20px mobile, with 30px intermediate margins. Product grids switch from four columns to two. The primary responsive threshold is 760px; additional refinements occur at 360px, 1100px and 1600px.

Controls are mostly square-edged. Colour swatches remain circular. Primary controls are 52px high, with mobile purchase controls at least 46px. Quantity controls and quick-option buttons use 44px targets. Focus outlines use 2px accent strokes with a 5px offset.

## 5. Component and behaviour specification

### Header and navigation

The brand returns home. Shop and collection links change hash routes without a server reload. The bag count reflects quantity, not just unique products. Dialogs close using the close button, Escape or a backdrop click. Focus is returned to the triggering control when it still exists.

### Product cards

Cards provide an image, product name, price, colour information and a clear route to product detail. The plus control opens the product-options page rather than silently selecting a default size. Image hover scaling is subtle and unnecessary for touch interaction. Product and availability content is explicitly illustrative.

### Search and collection filters

Search suggestions update while typing. Collection results support category, size, colour, maximum price and availability filters, as well as featured, ascending-price, descending-price and alphabetical sorting. Active filters are removable. Filters combine rather than replacing each other unexpectedly. Selecting availability with a size checks stock for that size. No-results recovery provides a direct way back to the collection.

Filter settings are represented in the route query string. The current implementation chooses one value per filter category. It is not a multi-select faceted-search backend.

### Product gallery, colours and sizing

Colour changes update the illustration and selected state. Sizes have available, selected and unavailable states. A product cannot be added without a valid available size. The error appears beside the size selector and focus moves to an available size.

The size guide offers sample centimetre/inch values. Measurements are fictional and must be replaced with approved, product-specific dimensions. Gallery controls show front and detail crops; touch swipes change the view. The zoom dialog enlarges the existing concept image, not undisclosed higher-resolution detail. All crop and recolouring limitations are labelled in the interface.

The mobile purchase bar is visible at the bottom of the viewport. It shows price and selection status, uses the same size validation as the main button and is accompanied by bottom page spacing so content is not permanently hidden.

### Bag and totals

Adding a product shows a short loading state followed by the bag drawer. The bag retains product, colour, size and quantity. Identical variants combine; different variants remain separate. Quantities cannot fall below one or exceed the sample stock limit. Removal is explicit. Empty-bag recovery links back to products.

The bag subtotal excludes delivery. Checkout adds the selected sample delivery charge. Illustrative taxes are included in sample prices; no real tax engine is present. Amounts are stored in integer minor units to avoid floating-point price accumulation.

### Checkout and confirmation

Checkout uses three steps: contact/address, delivery and review/payment. Field labels are persistent and validation is inline. Entered information survives step changes and simulated payment declines. A sample-details button avoids the need to use real personal information.

The payment page requests no card data. Two labelled test outcomes demonstrate approval and decline. Declining preserves the bag and details; approving creates only an in-memory demo receipt and clears the local demo bag. Confirmation explicitly says no payment was taken and no email was sent. The receipt is not proof of purchase.

### Newsletter and availability request

These forms demonstrate invalid and successful input states. They do not send or retain email addresses and do not create subscriptions or real stock notifications.

## 6. Accessibility and motion

Implemented measures include semantic landmarks, labelled controls, keyboard-operable buttons, visible focus styles, descriptive image alternatives, live feedback, inline validation, native modal focus containment and an explicit Escape handler. Size availability is conveyed by disabled state and text, not only colour. Loading buttons expose `aria-busy`.

Motion is restrained: 160ms control transitions and 240ms panels, with a 350ms product-image hover treatment. Reduced-motion preferences suppress these transitions. There is no automatic carousel, scroll hijacking or forced animation.

These are implementation measures, not a claim of WCAG certification. Native screen-reader testing, actual touch-hardware checks, full contrast auditing, 200% text resizing and cross-browser validation remain launch-review tasks.

## 7. Architecture, storage and privacy

The prototype uses plain HTML, CSS and JavaScript with no runtime package dependencies. Separate source files are the editable source of truth. `build.py` embeds them with the local JPEG assets into the portable HTML file. Routes use hash navigation, so a static host does not need application-route rewrites.

Only non-personal basket data is saved to local storage: product ID, size, colour and quantity. Stored data is validated against the catalogue, including unsupported IDs, invalid sizes and excessive quantities. Storage access failure falls back to the page session. Browser behaviour for `file:` local storage is not consistently specified; use a local HTTP origin to assess persistence.

Contact and address values remain in page memory. Refresh clears them. There is no network submission, analytics service, payment collection, customer database or authentication service. User-provided strings inserted into templates are HTML-escaped. These choices do not replace security review of a future production implementation.

## 8. Verification

The delivery passed 61 automated checks in headless Chromium. The harness loaded the self-contained HTML by local document injection, with no external network requests. It exercised product loading, sorting, filters, no-results recovery, missing-size errors, colour changes, size-unit conversion, gallery controls, bag quantities, checkout validation, shipping totals, decline recovery, confirmation, empty states, mobile navigation, focus return, reduced motion and mocked storage-sanitisation fixtures.

The homepage was checked for horizontal overflow at 320, 360, 390, 760, 768, 1100 and 1440px. Multiple other routes were checked at 390px. This does not establish that every browser, viewport or accessibility combination has been tested. See `qa-results.json` and the repeatable test script for exact scope.

Not tested: Safari, Firefox, physical phones, screen readers, real storage persistence across browser sessions, live payment/inventory/fulfilment integrations, customer usability and production asset quality.

## 9. Before launch

Replace the working brand name and all placeholder product content with approved business material. Obtain naming clearance and approved image usage rights. Replace low-resolution generated imagery with high-resolution campaign and product photographs, including each real colourway, front/back views and fabric details.

Connect an actual catalogue and stock source, server-authoritative pricing, destination-specific tax/shipping calculations, payment provider, order creation, confirmation email and fulfilment. Add account management only where needed. Define loading, timeout, stock-change, payment-cancellation and fulfilment-failure cases with the chosen services.

Approve privacy, terms, delivery, returns and contact information for the actual business and markets. Conduct customer usability sessions and accessibility/cross-browser testing. Optimise production image sizes and measure performance under realistic mobile-network conditions. The prototype's visual style is not a substitute for those launch requirements.

## Technical references

Primary documentation checked during preparation:

- [MDN: HTMLDialogElement.showModal()](https://developer.mozilla.org/en-US/docs/Web/API/HTMLDialogElement/showModal), for native modal behaviour.
- [MDN: Window.localStorage](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage), including the local-file behaviour caveat.
- [MDN: prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion), for motion preferences.

All screens and UI copy in this delivery are newly constructed for the VEXA concept. The campaign and product artwork is derived from the generated image already supplied in this conversation; no new external stock assets were included.
