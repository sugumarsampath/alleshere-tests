---
name: alleshere-domain
description: AllesHere application domain knowledge — what the site does, apps and data models, business rules, URL map, user flows, and UI selectors. Use when writing tests, reviewing tests, creating scenarios, or answering questions about how AllesHere behaves.
user-invocable: false
---

# AllesHere Domain Knowledge

## Overview
AllesHere ("Everything Here") is a commission-free community portal for Berlin —
tagline **"For all your local needs"**. v1 centres on **shared accommodation**
(WG rooms, private rooms, apartments), plus local directories (restaurants,
training, sports, services, jobs, immigration, events, daycare), a freelance
marketplace, content guides and banner ads.

- **Live site**: https://www.alleshere.de/ (always use `https://www.` form)
- **Local dev**: http://127.0.0.1:8000 (`.\venv\Scripts\python manage.py runserver` in the app repo)
- **App source**: `C:\Users\Brindha\Desktop\DreamProject` (Django package dir is `berlinnest/` — internal name)
- **This repo** (`alleshere-tests`) holds only the Playwright UI suite.

## Tech stack
- **Backend**: Django 6, Python 3.13, server-rendered templates
- **Frontend**: Tailwind CSS (CDN) + **HTMX** (live filtering on `/rooms/`), Leaflet/OpenStreetMap map on listing detail
- **DB**: PostgreSQL in prod, SQLite locally
- **Media**: Cloudinary
- **Auth**: Django sessions; email-as-username; Google sign-in via django-allauth
- **Hosting**: Railway; CI via GitHub Actions
- **Third-party scripts on every page**: Google Translate widget, Google Analytics 4, Cloudflare Web Analytics

## Django apps (source dirs in the app repo)
| App | Purpose |
|---|---|
| `listings` | Accommodation listings: home portal, browse, detail, create/edit/toggle/delete, My Listings |
| `accounts` | Register, login, logout, password reset |
| `messaging` | Seeker ↔ poster conversations about a listing, inbox, unread badge |
| `restaurants` / `training` | Business directories (own models) |
| `directory` | One model powering 6 categories: sports, local_services, jobs, immigration, events, daycare |
| `business` | "List your business" submission funnel (pending → admin approves) |
| `freelance` | Skill offers (auto-live) and company gigs (pending approval) + comments |
| `guides` | Student Tips, Learn German content pages |
| `ads` | Banner ads with click tracking, carousel |
| `contact` | Contact form → DB + email to admin |

## Detailed references (read as needed)
- [business-rules.md](business-rules.md) — rules to assert on (visibility, ownership, validation, moderation)
- [user-flows.md](user-flows.md) — step-by-step journeys for tests
- [ui-selectors.md](ui-selectors.md) — verified labels, roles, placeholders, IDs
- [url-map.md](url-map.md) — every route, auth requirement, and what it renders

## Core data models (summary)

### Listing (`listings.Listing`)
| Field | Notes |
|---|---|
| title | ≤120 chars, required |
| ad_type | `offered` "Room Offered" / `wanted` "Room Wanted" |
| description | required |
| district | one of 12 Berlin Bezirke (optional) |
| neighborhood, address | optional; address is shown publicly |
| room_type | `shared_room`, `private_room`, `studio`, `whole_flat` |
| gender_preference | `any` "Both" / `female` "Female only" / `male` "Male only" |
| rent_eur | required, positive int (warm rent) |
| deposit_eur | optional |
| available_from | required date |
| wifi_available, anmeldung_available, contract_available | booleans (✅/❌ on detail) |
| public_transport, supermarkets | free text (transport: one line each) |
| video_url | YouTube/Vimeo link → embedded; other hosts not embedded |
| status | `approved` default (auto-publish), `pending`, `rejected` |
| is_available | owner toggle: "Mark as taken" hides from search |
| is_featured | admin-only → purple "Featured" ribbon |
| images | `ListingImage`, many per listing |

### Conversation / Message (`messaging`)
One conversation per (listing, seeker). Poster = listing owner. Messages have `is_read`.

### Business entries (Restaurant, TrainingInstitute, DirectoryListing)
Share `BusinessSubmission` base: `status` (pending/approved/rejected), `is_active`, `submitted_by`, `contact_name`, `contact_email`.

### FreelancePost
`post_type` `skill` (auto-live) / `gig` (pending approval); title, description, skills (comma-separated), budget_eur, is_remote, contact_email; public `Comment`s.

### BannerAd
placement large/small, section (general/restaurants/training), schedule window, click_count, optional order buttons.

## The 12 districts (value → label)
mitte → Mitte · friedrichshain_kreuzberg → Friedrichshain-Kreuzberg · pankow → Pankow ·
charlottenburg_wilmersdorf → Charlottenburg-Wilmersdorf · spandau → Spandau ·
steglitz_zehlendorf → Steglitz-Zehlendorf · tempelhof_schoeneberg → Tempelhof-Schöneberg ·
neukoelln → Neukölln · treptow_koepenick → Treptow-Köpenick ·
marzahn_hellersdorf → Marzahn-Hellersdorf · lichtenberg → Lichtenberg ·
reinickendorf → Reinickendorf

## Keeping this skill current
The app changes often. Before relying on a rule or selector, confirm it in the
app source (`DreamProject/<app>/views.py`, `models.py`, `forms.py`,
`templates/`). If source and this skill disagree, **source wins** — update this
skill in the same change.
