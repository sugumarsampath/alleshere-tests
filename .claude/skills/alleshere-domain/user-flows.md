# AllesHere User Flows

Step-by-step journeys to base scenarios and tests on. **(L)** = local server
only (mutates data / sends email). Rule IDs → `business-rules.md`.

## F1 — Visitor browses rooms (prod-safe)
1. Open `/` → portal home with category cards and latest listings.
2. Click navbar "Accommodation" (or hover → "Shared Room" etc.).
3. On `/rooms/`, pick a district in the select → `#results` updates without reload, URL gains `?district=…` (BR-SRCH-4).
4. Type in "Search title…" → results update after ~400 ms.
5. Set Min €/Max € → only listings within range (BR-SRCH-1).
6. Click a card's "View More" → detail page with Description / Neighborhood / Location / Write a message.

## F2 — Register (L)
1. `/accounts/register/` → fill Email ID (unique, e.g. `qa+<ns>@example.com`), Password, Password confirmation.
2. Submit "Register" → redirected to `/`, flash "Welcome to AllesHere! Your account is ready.", navbar shows "Logout" (BR-AUTH-4).
- Negatives: weak password variants (BR-AUTH-3), duplicate email (BR-AUTH-2), mismatched confirmation.

## F3 — Login / logout (L)
1. `/accounts/login/` → Email ID + Password → "Login".
2. Lands on `/` (or `?next=`). Navbar shows "My Listings", "Messages", "Logout".
3. Click "Logout" → back to `/`, "Login"/"Register" visible.
- Negative: wrong password → "Incorrect email or password. Please try again." (BR-AUTH-5).

## F4 — Post a room (L)
1. Logged in, click "I have a place available" (→ `/listings/new/?ad_type=offered`) — Ad type pre-selected (BR-LST-10).
2. Fill Title (unique), Description, District, Room type, Rent, Available from (future date); optionally photos (`#id_images`), video URL.
3. "Submit Listing" → My Listings with flash "Your listing is now live! 🎉" (BR-LST-1).
4. Listing appears on `/rooms/` (search its title) and on its detail page.
- Guest clicking "+ Post Room" → redirected to login with `next=/listings/new/` (BR-LST-3).

## F5 — Manage own listing (L)
1. My Listings → "Edit" → change rent → "Save changes" → flash "Your listing was updated. ✅"; still public (BR-LST-5).
2. "Mark as taken" → hidden from `/rooms/` search, detail 404 for others, owner can still open it; button now "Mark available" (BR-LST-6, BR-LST-2).
3. "Mark available" → back in search.
4. "Delete" → confirm page → "Yes, delete permanently" → flash "Listing deleted.", gone from My Listings, detail 404 (BR-LST-7).

## F6 — Owner isolation (L, security)
1. User A posts a listing (note its id).
2. User B (separate browser context) opens `/listings/<id>/edit/`, `/listings/<id>/delete/` → 404 (BR-LST-4).
3. Anonymous opens the same → redirected to login.

## F7 — Messaging between seeker and poster (L)
1. Poster (context A) posts a listing.
2. Seeker (context B) opens it → "💬 Send Message" → thread page.
3. Seeker types in "Type a message…" → "Send" → message appears.
4. Poster reloads → navbar "Messages" shows unread badge "1" (BR-MSG-6); opens inbox → thread → badge clears.
5. Poster replies; seeker sees it.
- Guest sees "💬 Login to Send Message" (BR-MSG-1); owner sees own-listing text (BR-MSG-2); third user opening the thread URL → 404 (BR-MSG-4).

## F8 — Contact us (GET prod-safe, POST L)
1. Footer "Contact us" → `/contact/`.
2. Fill Name, Email ID, Description (Phone optional) → "Send message".
3. Flash "Thanks for reaching out! We'll get back to you soon." (BR-CT-2).
- Negatives: empty required fields, invalid email → field errors, no email sent.

## F9 — Directories (prod-safe)
1. Navbar "More" → "🍽️ Restaurants" (or any category).
2. Search by name/cuisine; filter district (directory categories include city-wide entries, BR-DIR-3).
3. Open an entry → business detail page with back link to the category.

## F10 — List your business (L)
1. Logged in → "➕ List your business" → choose type → fill form incl. contact email (required).
2. Submit → `/business/mine/` shows it as "Pending approval"; it is **not** on the public list (BR-BIZ-3).

## F11 — Freelance (GET prod-safe, POST L)
1. `/freelance/` → filter Skills vs Gigs, search.
2. Post a skill offer → live immediately; post a gig → pending, only owner can open it (BR-FL-1..3).
3. Comment on a post (logged in) → "Comment posted."

## F12 — Password reset (L)
1. Login page → "Forgot password?" → enter Email ID → "sent" page.
2. Only verifiable end-to-end with the console email backend locally (read link from server output) — otherwise assert up to the "sent" page.

## F13 — Mobile navigation (prod-safe)
1. Viewport 375×812 → desktop nav hidden; "Login"/"Sign up" in top bar.
2. Tap "Open menu" → `#mobileNav` shows category links and language slot.
3. No horizontal scroll on key pages.
