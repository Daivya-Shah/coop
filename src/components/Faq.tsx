"use client";

import { Accordion } from "@base-ui/react/accordion";
import { FAQ } from "@/content/coop";
import { Plus } from "./Plus";

export function Faq() {
  return (
    <Accordion.Root className="faq">
      {FAQ.map((f) => (
        <Accordion.Item key={f.q} className="faq-item">
          <Accordion.Header className="faq-head">
            <Accordion.Trigger className="faq-trigger">
              {f.q}
              <Plus />
            </Accordion.Trigger>
          </Accordion.Header>
          <Accordion.Panel className="faq-panel">
            <p>{f.a}</p>
          </Accordion.Panel>
        </Accordion.Item>
      ))}
    </Accordion.Root>
  );
}
