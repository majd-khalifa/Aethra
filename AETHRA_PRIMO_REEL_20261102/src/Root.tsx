import { Composition } from "remotion";
import { PrimoReel } from "./Reel";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="AethraPrimo"
        component={PrimoReel}
        width={1080}
        height={1920}
        fps={30}
        durationInFrames={600}
      />
    </>
  );
};
