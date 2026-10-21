"use client";

import { createContext, useCallback, useContext, useEffect, useState } from "react";
import { Dialog } from "@base-ui/react/dialog";
import { Tabs } from "@base-ui/react/tabs";
import { MotionConfig } from "motion/react";
import { Toaster } from "sonner";
import { Plus } from "./Plus";
import { ClubForm, VenueForm } from "./IntakeForm";

export type Side = "venue" | "club";

const JoinContext = createContext<(side: Side) => void>(() => {});

/** Wraps the site so any "I run a venue / club" button can open the join panel. */
export function JoinProvider({ children }: { children: React.ReactNode }) {
  const [side, setSide] = useState<Side>("venue");
  const [open, setOpen] = useState(false);

  const openJoin = useCallback((s: Side) => {
    setSide(s);
    setOpen(true);
  }, []);

  // Deep link: coop.nyc/#join
  useEffect(() => {
    if (location.hash === "#join") openJoin("venue");
  }, [openJoin]);

  return (
    <JoinContext.Provider value={openJoin}>
      <MotionConfig reducedMotion="user">{children}</MotionConfig>
      <Dialog.Root open={open} onOpenChange={setOpen}>
        <Dialog.Portal>
          <Dialog.Backdrop className="panel-backdrop" />
          <Dialog.Popup className="panel">
            <Dialog.Close className="close" aria-label="Close"><Plus /></Dialog.Close>
            <div className="panel-body">
              <div>
                <Dialog.Title className="panel-title">Join the Pilot</Dialog.Title>
                <Dialog.Description className="lede">Two minutes. No account.</Dialog.Description>
                <Tabs.Root value={side} onValueChange={(v) => setSide(v as Side)}>
                  <Tabs.List className="switch" aria-label="Which side are you on?">
                    <Tabs.Tab value="venue">I run a venue</Tabs.Tab>
                    <Tabs.Tab value="club">I run a club</Tabs.Tab>
                    <Tabs.Indicator className="switch-dot" data-side={side} />
                  </Tabs.List>
                  <Tabs.Panel value="venue"><VenueForm onSent={() => setOpen(false)} /></Tabs.Panel>
                  <Tabs.Panel value="club"><ClubForm onSent={() => setOpen(false)} /></Tabs.Panel>
                </Tabs.Root>
              </div>
              <img className="panel-sketch" src="/img/sketches/name-tags.svg" alt="" />
            </div>
          </Dialog.Popup>
        </Dialog.Portal>
      </Dialog.Root>
      <Toaster
        position="bottom-center"
        toastOptions={{ className: "coop-toast" }}
      />
    </JoinContext.Provider>
  );
}

export function JoinButton({ side, className, children }: { side: Side; className?: string; children: React.ReactNode }) {
  const openJoin = useContext(JoinContext);
  return <button className={className} onClick={() => openJoin(side)}>{children}</button>;
}
