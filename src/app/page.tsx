import { FlipThrough } from "@/components/FlipThrough";
import { TopBar } from "@/components/TopBar";

export default function Home() {
  return (
    <>
      <TopBar page="landing" />
      <FlipThrough />
    </>
  );
}
