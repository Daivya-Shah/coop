"use client";

import { useState } from "react";
import { toast } from "sonner";

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
      const bad = !input.value.trim() || (input.type === "email" && !input.validity.valid);
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
      const name = String(data.get("name")).trim().split(" ")[0];
      toast(`Thanks, ${name}, got it. We'll be in touch about the pilot.`);
      form.reset();
      onSent();
    } catch {
      toast("Something went wrong sending that. Please try again in a minute.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <form className="intake" noValidate onSubmit={submit}>
      {children}
      <button className="pill" type="submit" disabled={busy}>Send it</button>
      <p className="small">{note}</p>
    </form>
  );
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return <label><span>{label}</span>{children}</label>;
}

function Select({ name, options }: { name: string; options: string[] }) {
  return <select name={name}>{options.map((o) => <option key={o}>{o}</option>)}</select>;
}

const NIGHTS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

export function VenueForm({ onSent }: { onSent: () => void }) {
  return (
    <IntakeForm side="venue" onSent={onSent} note="Sending this isn't a booking. We'll only use it to talk to you about the pilot.">
      <Field label="Venue name"><input name="venue" required autoComplete="organization" /></Field>
      <Field label="Your name"><input name="name" required autoComplete="name" /></Field>
      <Field label="Email"><input name="email" type="email" required autoComplete="email" /></Field>
      <Field label="Neighborhood">
        <Select name="area" options={["Chelsea", "Flatiron", "East Village", "Lower East Side", "Somewhere else"]} />
      </Field>
      <fieldset>
        <legend>Your quiet nights</legend>
        <div className="chips">
          {NIGHTS.map((n) => (
            <label key={n}><input type="checkbox" name="nights" value={n} /><span>{n}</span></label>
          ))}
        </div>
      </fieldset>
      <Field label="Group size you could host">
        <Select name="capacity" options={["10–20", "20–30", "30–40", "40+"]} />
      </Field>
    </IntakeForm>
  );
}

export function ClubForm({ onSent }: { onSent: () => void }) {
  return (
    <IntakeForm side="club" onSent={onSent} note="Free for clubs. You can turn down any match.">
      <Field label="Club name"><input name="club" required /></Field>
      <Field label="Your name"><input name="name" required autoComplete="name" /></Field>
      <Field label="Email"><input name="email" type="email" required autoComplete="email" /></Field>
      <Field label="Instagram or link"><input name="link" placeholder="@yourclub" /></Field>
      <Field label="What do you do?">
        <Select
          name="type"
          options={["Run club", "Book club", "Craft night", "Game night", "Language exchange", "Supper club", "Writing group", "Wellness group", "Something else"]}
        />
      </Field>
      <Field label="How many usually show up?">
        <Select name="turnout" options={["Under 10", "10–20", "20–35", "35+"]} />
      </Field>
      <Field label="How often?">
        <Select name="cadence" options={["Weekly", "Every other week", "Monthly"]} />
      </Field>
    </IntakeForm>
  );
}
