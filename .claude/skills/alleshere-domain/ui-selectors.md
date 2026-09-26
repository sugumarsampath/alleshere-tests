# AllesHere UI Selectors

Verified against the Django templates in `DreamProject/templates/`. Python
`pytest-playwright` syntax. The site has **no `data-testid` attributes yet** —
where a test needs one, add it to the template in the app repo.

Django form fields render with `id="id_<field_name>"` and a `<label for>`, so
`get_by_label(...)` works for every form field below.

## Navbar (`base.html`)
Desktop (≥768 px) and a separate mobile menu both exist in the DOM, so the same
link text appears twice → scope to `page.locator("nav")` and use `.first`, or
check the visible one.
- Home/logo: `page.locator("nav").get_by_role("link").first` (href `/`)
- Accommodation dropdown trigger: `get_by_role("link", name="Accommodation")` — items appear on **hover**: "All Accommodation", "Shared Room", "Private Room", "Apartments", pills "I need a place to live", "I have a place available"
- More dropdown (hover the text "More"): "🍽️ Restaurants", "🎓 Training", "📘 Student Tips", "🗣️ Learn German", "🏃 Berlin Marathon Guide", "⚽ Sports", "🛠️ Local Services", "💼 Jobs", "🛂 Immigration", "🎉 Events", "🧸 Daycare & Nanny", "💻 Freelance", "➕ List your business"
- Logged out: links "+ Post Room", "Login", "Register" (mobile top bar: "Login", "Sign up")
- Logged in: links "My Listings", "Messages" (+ unread badge number), "+ Post Room"; button "Logout"
- Mobile menu: button `get_by_role("button", name="Open menu")` toggles `#mobileNav`
- Language widget: `#google_translate_element` (third-party — don't assert its internals)

## Flash messages
Rendered in `base.html` from Django messages — assert with
`expect(page.get_by_text("Your listing is now live!")).to_be_visible()`.

## Accommodation browse `/rooms/`
- Heading: `get_by_role("heading", name="Accommodation in Berlin")`
- Intent pills: links "I need a place to live", "I have a place available"
- Room-type chips: links "All", "Shared Room", "Private Room", "Apartments"
- Search: `get_by_placeholder("Search title…")` (name `q`, note the `…` character)
- District select: `page.locator("select[name='district']")` (first option "All districts")
- Room type select: `page.locator("select[name='room_type']")` (first option "Any type")
- Price: `get_by_placeholder("Min €")`, `get_by_placeholder("Max €")`
- District quick-link chips: links with district labels, after "Popular districts:"
- Results container: `#results` (HTMX swap target)
- Count: `get_by_text(re.compile(r"\d+ listings? found"))`
- Empty: `get_by_text("No listings match your filters.")`
- Card: no testid yet — card title is an `h3`; each card has link "View More"
- Pagination links use `hx-get` inside `#results`

## Listing detail `/listings/<id>/`
- Title: `get_by_role("heading", level=1)`
- Section headings (h2): "Description", "Neighborhood", "Location", "Write a message"
- Main photo: `#main-photo`; map: `#listing-map`
- Google Maps link: `get_by_role("link", name=re.compile("Open in Google Maps"))`
- Message CTA: logged-in non-owner → link "💬 Send Message"; guest → link "💬 Login to Send Message"; owner → text "This is your own listing."
- Back link: "← Back to all listings"

## Post / edit listing `/listings/new/`, `/listings/<id>/edit/`
- Heading: "Post a Room or Flat" / "Edit your listing"
- Fields (labels from model verbose names): "Title", "Ad type", "Description", "District", "Neighborhood", "Address", "Room type", "Gender preference", "Rent eur", "Deposit eur", "Available from", "WiFi available", "Anmeldung possible", "Contract available", "Public connections", "Supermarkets", "Video url" — **prefer `#id_<field>`** (`#id_rent_eur`, `#id_available_from`…) if a label is ambiguous
- Photos: `#id_images` (multiple file input) → `set_input_files([...])`
- Submit: `get_by_role("button", name="Submit Listing")` / `name="Save changes"`
- Edit Cancel: link "Cancel"

## My Listings `/listings/mine/`
- Heading: "My Listings"
- Per row: link "Edit", button "Mark as taken" / "Mark available", link "Delete"
- Row title link = listing title → scope actions: `page.locator("div").filter(has=page.get_by_role("link", name=title))` (better: add `data-testid="my-listing-row"`)
- Empty: link "Post your first room →"

## Delete confirm
- Heading "Delete this listing?"; button "Yes, delete permanently"; link "Cancel"

## Auth
- Login `/accounts/login/`: heading "Login"; `get_by_label("Email ID")` (placeholder "you@example.com"); `get_by_label("Password")`; show/hide button `name="Show password"`; link "Forgot password?"; submit `get_by_role("button", name="Login")`; link "Register"
- Register `/accounts/register/`: heading "Create an Account"; `get_by_label("Email ID")`; `#id_password1`, `#id_password2` (labels "Password" / "Password confirmation" — use IDs to avoid strict-mode clash); submit `get_by_role("button", name="Register")`
- Google button present (`accounts/_google_button.html`) — never click in tests

## Messaging
- Inbox `/messages/`: heading "Messages"; each conversation is a link to `/messages/<id>/`
- Thread: input `get_by_placeholder("Type a message…")`; `get_by_role("button", name="Send")`; link "← Inbox"

## Contact `/contact/`
- Heading "Send us a message" (h2)
- `get_by_label("Name")`, `get_by_label("Email ID")`, `get_by_label("Phone number")`, `get_by_label("Description")`, photos `#id_photos`
- Submit: `get_by_role("button", name="Send message")` (lowercase m — different from the listing "💬 Send Message")

## Directories
- Restaurants / Training / directory lists: search input name `q`, `select[name='district']`
- Business detail: shared template `pages/business_detail.html`

## Other pages
- Marathon guide: `#countdown`, `#marathonMap`
- Banner carousel: `#ad-track`, dots `#ad-dots` (only when >1 ad)
