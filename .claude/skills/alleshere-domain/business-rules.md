# AllesHere Business Rules

Rules derived from the app source (`DreamProject`). Each has an ID so scenarios
and tests can trace back to it. Source file in brackets.

## Accounts (`accounts/forms.py`, `accounts/validators.py`, `accounts/views.py`)
- **BR-AUTH-1** Registration uses **email as the username** (lowercased). Label is "Email ID".
- **BR-AUTH-2** Duplicate email (case-insensitive) → "An account with this email already exists. Try logging in instead."
- **BR-AUTH-3** Password: **min 7, max 16 chars, ≥1 capital letter, ≥1 number** (plus Django's common/numeric/similarity validators). Errors: "Password must contain at least 1 capital letter.", "Password must contain at least 1 number.", "Password must be at most 16 characters."
- **BR-AUTH-4** Successful registration logs the user in, redirects to `/`, flash "Welcome to AllesHere! Your account is ready."
- **BR-AUTH-5** Wrong login → "Incorrect email or password. Please try again."
- **BR-AUTH-6** Login redirects to `?next=` if it is a same-site path, else `/`. External or scheme-relative targets (`https://evil.example`, `//evil.example`) fall back to `/` (open-redirect protection — cover it with a Security scenario).
- **BR-AUTH-7** Logout is a **POST** form (navbar "Logout" button), redirects to `/`.
- **BR-AUTH-8** Password reset via email (`/accounts/password-reset/`); sends real email through Gmail SMTP when configured → **local only**, and the link uses the request host.

## Listings (`listings/views.py`, `listings/models.py`)
- **BR-LST-1** **Auto-publish**: a new listing is `approved` and live immediately; flash "Your listing is now live! 🎉", redirect to My Listings.
- **BR-LST-2** Public = `status == approved` **and** `is_available`. Pending/rejected/taken listings are hidden from home, browse and detail (404) — **except the owner** can still open their own detail page.
- **BR-LST-3** Posting, editing, toggling, deleting and My Listings require login (anon → redirect to `/accounts/login/?next=…`).
- **BR-LST-4** Edit/toggle/delete are **owner-only**; another user gets **404**, not 403.
- **BR-LST-5** Editing keeps the listing live (status → approved) **unless an admin had rejected it** (stays rejected). Flash "Your listing was updated. ✅".
- **BR-LST-6** "Mark as taken" sets `is_available=False` → hidden from search, still in My Listings; button flips to "Mark available". Flashes: "Listing marked as taken and hidden from search." / "Listing is available again and back in search. ✅"
- **BR-LST-7** Delete has a confirm page ("Delete this listing?" → "Yes, delete permanently"); irreversible; flash "Listing deleted."
- **BR-LST-8** Photos: multiple uploads; only `image/*` ≤ **5 MB** kept; others skipped with warning "N file(s) were skipped — images only, max 5 MB each." Listing still saves.
- **BR-LST-9** In edit mode each existing photo has a remove checkbox (`delete_image_<id>`).
- **BR-LST-10** `?ad_type=wanted|offered` on `/listings/new/` pre-selects Ad type ("I need a place to live" → wanted, "I have a place available" → offered). Invalid values are ignored.
- **BR-LST-11** Video: YouTube (`watch?v=`, `youtu.be/`) and Vimeo links embed; any other URL shows no embed.
- **BR-LST-12** Detail map shows the **district centre with a privacy circle**, never the exact address; "Open in Google Maps" uses the address if given, else "<District>, Berlin".
- **BR-LST-13** Featured (admin-set) listings show a "Featured" ribbon on the card.

## Browse & search (`/rooms/`, `listings.views.browse`)
- **BR-SRCH-1** Filters: `q` (title/description/neighborhood, case-insensitive), `district`, `room_type`, `category` (`roommates`=shared+private, `rentals`/`apartments`=studio+whole flat), `min_price`, `max_price` (inclusive, rent_eur).
- **BR-SRCH-2** Non-numeric price values are **ignored** (no error).
- **BR-SRCH-3** Unknown `category` is ignored (shows all).
- **BR-SRCH-4** Filter form uses **HTMX**: changes swap only `#results` and push the URL (`hx-push-url`); text/price inputs debounce 400 ms.
- **BR-SRCH-5** **12 per page**; pagination keeps active filters.
- **BR-SRCH-6** Result count text: "N listing(s) found"; empty → "No listings match your filters."
- **BR-SRCH-7** Newest first (`-created_at`).

## Messaging (`messaging/`)
- **BR-MSG-1** Only logged-in users can message; guests see "💬 Login to Send Message" → login with `next` back to the listing.
- **BR-MSG-2** Owner sees "This is your own listing. Seekers will contact you here." (no button). Hitting `/messages/start/<id>/` on own listing → error flash "You can't message yourself about your own listing."
- **BR-MSG-3** One conversation per (listing, seeker) — starting again reopens the same thread.
- **BR-MSG-4** Only the two participants can view a thread; anyone else → 404.
- **BR-MSG-5** Empty/whitespace message is ignored (no message created).
- **BR-MSG-6** Opening a thread marks the other person's messages read; navbar "Messages" shows an unread count badge.
- **BR-MSG-7** Starting a conversation requires the listing to be `approved` (404 otherwise). Note: it does **not** check `is_available`.

## Directories (restaurants, training, 6 directory categories)
- **BR-DIR-1** Public entries: `status == approved` **and** `is_active`.
- **BR-DIR-2** Search `q` matches name + cuisine (restaurants) / subject (training) / subtitle (directory).
- **BR-DIR-3** Directory district filter **also includes city-wide entries** (district blank = "All districts").
- **BR-DIR-4** Detail pages 404 for non-live entries.

## Business submissions (`/business/`)
- **BR-BIZ-1** Login required. `/business/new/<type>/` where type ∈ restaurant, training, sports, local_services, jobs, immigration, events, daycare; unknown type → 404.
- **BR-BIZ-2** Contact email is **required**.
- **BR-BIZ-3** Submissions are **PENDING** (hidden) until admin approval; flash "Thanks! Your business has been submitted for review…", redirect to `/business/mine/` which lists status.

## Freelance (`/freelance/`)
- **BR-FL-1** Skill offer (`/freelance/new/skill/`) → live immediately: "Your skill post is now live! 🎉".
- **BR-FL-2** Company gig (`/freelance/new/gig/`) → pending: "Thanks! Your gig was submitted for review…".
- **BR-FL-3** Pending/rejected posts visible only to owner; others 404.
- **BR-FL-4** Comments: logged-in only (anon POST → login redirect); flash "Comment posted."
- **BR-FL-5** List filters by `?type=skill|gig` and `?q=` (title/description/skills).

## Contact (`/contact/`)
- **BR-CT-1** Fields: Name, Email ID, Phone number (optional), Description, optional photos.
- **BR-CT-2** Submit saves to DB **and emails the admin** (reply-to = sender) → **local only**. Success flash "Thanks for reaching out! We'll get back to you soon."
- **BR-CT-3** Logged-in users get email (and name if set) pre-filled.
- **BR-CT-4** No phone number is published on the site (deliberate).

## Ads
- **BR-AD-1** Home carousel rotates all live large ads; `/restaurants/` and `/training/` show only their section's ads.
- **BR-AD-2** Ad clicks go through `/ads/<pk>/click/` (increments click_count, redirects to advertiser) — **don't click ads against production** (skews real advertiser stats).
- **BR-AD-3** Carousel arrows/dots only render when more than one ad is live; auto-advance 5 s.

## Content / seasonal
- **BR-CNT-1** Homepage Berlin Marathon banner shows only **until 2026-09-28**.
- **BR-CNT-2** Guides pages show an "coming soon" empty message when no published entries.
- **BR-CNT-3** `robots.txt` disallows `/admin/` and points to `/sitemap.xml`.
