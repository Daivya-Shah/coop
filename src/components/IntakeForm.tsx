"use client";

import { useState } from "react";
import { toast } from "sonner";
import { DAYS, NEIGHBORHOODS, PRIVACY, THANKS } from "@/content/coop";

// Form service URLs (e.g. Formspree). Left empty, submissions stay in the browser.
const ENDPOINTS = {
  venue: process.env.NEXT_PUBLIC_FORM_VENUE ?? "",
  club: process.env.NEXT_PUBLIC_FORM_CLUB ?? "",
};

type Props = { side: "venue" | "club"; note: string; onSent: () => void; children: React.ReactNode };

function IntakeForm({ side, note, onSent, children }: Props) {
  const [busy, setBusy] = useState(false);

  async function submit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const form = e.currentTarget;

    let ok = true;
    form.querySelectorAll<HTMLInputElement>("[required]").forEach((input) => {
      const bad = input.type === "checkbox"
        ? !input.checked
        : !input.value.trim() || (input.type === "email" && !input.validity.valid);
      input.setAttribute("aria-invalid", String(bad));
      if (bad && ok) { input.focus(); ok = false; }
    });
    if (!ok) return;

    const data = new FormData(form);
    setBusy(true);
    try {
      const endpoint = ENDPOINTS[side];
      if (endpoint) {
        const res = await fetch(endpoint, { method: "POST", body: data, headers: { Accept: "application/json" } });
        if (!res.ok) throw new Error(res.statusText);
      } else {
        console.warn("Coop intake form has no endpoint; submission was not sent.", Object.fromEntries(data));
      }
      toast(THANKS);
      form.reset();
      onSent();
    } catch {
      toast("That didn’t go through. Please try again in a minute; nothing you typed was lost.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <form className="intake" noValidate onSubmit={submit}>
      {children}
      <label className="consent">
        <input type="checkbox" name="consent" required />
        <span>You can contact me about the Coop pilot. {PRIVACY}</span>
      </label>
      <button className="pill" type="submit" disabled={busy}>{busy ? "Sending…" : "Send it"}</button>
      <p className="small">{note}</p>
    </form>
  );
}

function Field({ label, children, wide }: { label: string; children: React.ReactNode; wide?: boolean }) {
  return <label className={wide ? "wide" : undefined}><span>{label}</span>{children}</label>;
}

function Select({ name, options }: { name: string; options: string[] }) {
  return <select name={name}>{options.map((o) => <option key={o}>{o}</option>)}</select>;
}

function Chips({ legend, name, options }: { legend: string; name: string; options: string[] }) {
  return (
    <fieldset className="wide">
      <legend>{legend}</legend>
      <div className="chips">
        {options.map((o) => (
          <label key={o}><input type="checkbox" name={name} value={o} /><span>{o}</span></label>
        ))}
      </div>
    </fieldset>
  );
}

export function VenueForm({ onSent }: { onSent: () => void }) {
  return (
    <IntakeForm side="venue" onSent={onSent} note="Sending this isn’t a booking, and there’s no fee to join the pilot.">
      <Field label="Venue name"><input name="venue" required autoComplete="organization" /></Field>
      <Field label="What kind of place?"><Select name="venueType" options={["Restaurant", "Bar", "Café", "Something else"]} /></Field>
      <Field label="Neighborhood"><Select name="area" options={NEIGHBORHOODS} /></Field>
      <Field label="Your name"><input name="name" required autoComplete="name" /></Field>
      <Field label="Business email"><input name="email" type="email" required autoComplete="email" /></Field>
      <Field label="Phone (optional)"><input name="phone" type="tel" autoComplete="tel" inputMode="tel" /></Field>
      <Chips legend="Nights that could use a crowd" name="nights" options={DAYS} />
      <Field label="Group size you could host"><Select name="capacity" options={["Up to 10", "10–20", "20–30", "30–40", "40+"]} /></Field>
      <Field label="Open to a four-week trial?"><Select name="trial" options={["Yes", "Maybe, let’s talk", "Not yet"]} /></Field>
      <Chips legend="The space" name="space" options={["Seated tables", "One long table", "A private room", "Bar seating"]} />
    </IntakeForm>
  );
}

export function ClubForm({ onSent }: { onSent: () => void }) {
  return (
    <IntakeForm side="club" onSent={onSent} note="Free for clubs. You can turn down any match.">
      <Field label="Club name"><input name="club" required /></Field>
      <Field label="What do you do?">
        <Select
          name="activity"
          options={["Run club", "Book club", "Chess or board games", "Crafts, knitting or art", "Language exchange", "Writing group", "Supper club", "Something else"]}
        />
      </Field>
      <Field label="Your name"><input name="name" required autoComplete="name" /></Field>
      <Field label="Email"><input name="email" type="email" required autoComplete="email" /></Field>
      <Field label="Instagram or website (optional)" wide><input name="link" placeholder="@yourclub" autoCapitalize="none" /></Field>
      <Field label="How many actually show up?"><Select name="turnout" options={["Under 10", "10–20", "20–35", "35+"]} /></Field>
      <Field label="How often?"><Select name="cadence" options={["Weekly", "Every other week", "Monthly"]} /></Field>
      <Chips legend="Neighborhoods that work" name="areas" options={NEIGHBORHOODS} />
      <Chips legend="Days that work" name="days" options={DAYS} />
      <Field label="Anything a venue should know? (optional)" wide>
        <textarea name="needs" rows={2} placeholder="Tables, quiet corner, step-free access, a projector…" />
      </Field>
    </IntakeForm>
  );
}
