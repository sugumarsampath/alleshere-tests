# AllesHere URL Map

AllesHere has **no JSON API yet** (planned later with DRF). Every route returns
HTML. "Auth" = login required (anon → `/accounts/login/?next=<path>`).
"Local only" = mutates data or sends email — never exercise against production.

| Path | Auth | Renders / does | Prod-safe? |
|---|---|---|---|
| `/` | – | Portal home: hero, search, category cards, latest listings | ✅ |
| `/rooms/` | – | Browse accommodation + HTMX filters (`q`, `district`, `room_type`, `category`, `min_price`, `max_price`, `page`) | ✅ |
| `/listings/<id>/` | – | Listing detail (404 if not public, unless owner) | ✅ |
| `/listings/new/` | ✅ | Post form (`?ad_type=wanted|offered`) | GET ✅ / POST local |
| `/listings/mine/` | ✅ | My Listings | local |
| `/listings/<id>/edit/` | ✅ owner | Edit form | local |
| `/listings/<id>/toggle/` | ✅ owner | POST: mark taken/available | local |
| `/listings/<id>/delete/` | ✅ owner | Confirm page, POST deletes | local |
| `/accounts/register/` | – | Register form | GET ✅ / POST local |
| `/accounts/login/` | – | Login form (+ Google button) | GET ✅ / POST local |
| `/accounts/logout/` | – | POST logs out | local |
| `/accounts/password-reset/` (+ `sent/`, `<uid>/<token>/`, `done/`) | – | Password reset flow (sends email) | GET ✅ / POST local |
| `/accounts/google/login/` … | – | allauth Google OAuth | ❌ don't automate |
| `/messages/` | ✅ | Inbox | local |
| `/messages/start/<listing_id>/` | ✅ | Create/reopen conversation → thread | local |
| `/messages/<id>/` | ✅ participant | Thread + send form | local |
| `/restaurants/`, `/restaurants/<id>/` | – | Directory list (`q`, `district`) / detail | ✅ |
| `/training/`, `/training/<id>/` | – | Directory list / detail | ✅ |
| `/sports/` `/local-services/` `/jobs/` `/immigration/` `/events/` `/daycare/` | – | Directory category list (`q`, `district`) | ✅ |
| `/directory/<id>/` | – | Directory entry detail | ✅ |
| `/business/` | ✅ | Choose business type | local |
| `/business/new/<type>/` | ✅ | Submit business (pending) | local |
| `/business/mine/` | ✅ | My submissions + status | local |
| `/freelance/` | – | Freelance list (`type=skill|gig`, `q`) | ✅ |
| `/freelance/new/<skill|gig>/` | ✅ | Create post | local |
| `/freelance/<id>/` | – | Detail + comments (POST comment needs login) | GET ✅ |
| `/freelance/mine/` | ✅ | My posts | local |
| `/student-tips/`, `/learn-german/` | – | Guides | ✅ |
| `/berlin-marathon/` | – | Marathon guide (countdown, map) | ✅ |
| `/about/`, `/privacy/`, `/impressum/` | – | Static pages | ✅ |
| `/contact/` | – | Contact form (POST sends email) | GET ✅ / POST local |
| `/ads/<id>/click/` | – | Click-track redirect to advertiser | ❌ (skews stats) |
| `/sitemap.xml`, `/robots.txt` | – | SEO files | ✅ |
| `/admin/` | staff | Django admin | ❌ |
