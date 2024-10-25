import { useEffect } from "react";
import {
  CircleStackIcon,
  WrenchScrewdriverIcon,
  ComputerDesktopIcon,
  VideoCameraIcon,
  PhotoIcon,
} from "@heroicons/react/20/solid";
import AOS from "aos";
import "aos/dist/aos.css";
const features = [
  {
    name: "Model:",
    description: "MTCNN",
    icon: ComputerDesktopIcon,
  },
  {
    name: "Architecture",
    description: "InceptionResnetV1",
    icon: WrenchScrewdriverIcon,
  },
  {
    name: "Dataset:",
    description: "VGGFace2",
    icon: CircleStackIcon,
  },
];

export default function About() {
  useEffect(() => {
    AOS.init({ duration: 2000 });
  }, []);
  return (
    <div
      className="relative isolate overflow-hidden  px-6 py-24 sm:py-32 lg:overflow-visible lg:px-0"
      id="about"
    >
      <div className="mx-auto grid max-w-2xl grid-cols-1 gap-x-8 gap-y-16 lg:mx-0 lg:max-w-none lg:grid-cols-2 lg:items-start lg:gap-y-10">
        <div className="lg:col-span-2 lg:col-start-1 lg:row-start-1 lg:mx-auto lg:grid lg:w-full lg:max-w-7xl lg:grid-cols-2 lg:gap-x-8 lg:px-8">
          <div className="lg:pr-4">
            <div className="lg:max-w-lg">
              <h2 className="text-lg leading-7">Get to know more</h2>
              <p className="mt-2 text-4xl font-bold tracking-tight sm:text-6xl">
                About DeepFake
              </p>
              <p className="mt-6 text-lg leading-8" data-aos="fade-right">
              Deepfakes have emerged as a significant phenomenon in the world of synthetic media, 
              driven by advances in deep learning techniques. 
              At the core of deepfakes lies the ability to convincingly alter visual content, most notably through face-swapping, 
              where one person's face is seamlessly superimposed onto another's in videos or images.
              While deepfakes have legitimate applications in entertainment and visual effects, their potential for misuse has raised widespread concerns. 
              These concerns revolve around issues such as misinformation, identity theft, and reputational damage, 
              as deepfakes can be used to create highly realistic but entirely fabricated content. 
              Despite the risks, continued research and innovation in deepfake technology are essential, both to harness their potential benefits and to safeguard against their harmful consequences.
              </p>
            </div>
          </div>
        </div>
        <div
          className="-ml-12 -mt-12 p-12 lg:col-start-2 lg:row-span-2 lg:row-start-1 lg:overflow-hidden"
          data-aos="fade-left"
        >
          <img
            className="w-[38rem] ring-2 ring-base-300 max-w-none rounded-xl shadow-xl sm:w-[57rem]"
            src="https://cdn.dribbble.com/users/32512/screenshots/6495831/face_id2_effect_by_gleb.gif"
            alt="Person"
          />
        </div>
      </div>
      <div className="mx-auto grid max-w-2xl grid-cols-1 gap-x-8 gap-y-16 lg:mx-0 lg:max-w-none lg:grid-cols-2 lg:items-start lg:gap-y-10">
        <div className="lg:col-span-2 lg:col-start-1 lg:mx-auto lg:grid lg:w-full lg:max-w-7xl lg:gap-x-8 lg:px-8">
          <div className="text-base leading-7">
            <div className="grid gap-x-6 sm:grid-cols-2">
              <div
                className="ring-2 ring-base-300 bg-base-200 rounded-2xl mt-10 p-5 shadow-xl"
                data-aos="zoom-in"
              >
                <PhotoIcon className="h-5 w-5 mx-auto" aria-hidden="true" />
                <h2 className=" text-2xl text-center font-bold tracking-tight">
                  Image DeepFake
                </h2>
                <p className="mt-3 list-item list-inside">
                Facial landmarks: Key points such as eyes, nose, and mouth.
                </p>
                <p className="mt-3 list-item list-inside">
                Facial texture: Skin texture, pores, and wrinkles.
                </p>
                <p className="mt-3 list-item list-inside">
                Movement of facial muscles and changes in expression intensity.
                </p>
              </div>
              <div
                className="ring-2 ring-base-300 bg-base-200 rounded-2xl mt-10 p-5 shadow-xl"
                data-aos="zoom-in"
              >
                <VideoCameraIcon
                  className="h-5 w-5 mx-auto"
                  aria-hidden="true"
                />
                <h2 className=" text-2xl text-center font-bold tracking-tigh">
                  Video DeepFake
                </h2>
                <p className="mt-3 list-item list-inside">
                Facial landmarks: Key points such as eyes, nose, and mouth.
                </p>
                <p className="mt-3 list-item list-inside">
                Lip movement synchronization.
                </p>
                <p className="mt-3 list-item list-inside">
                Capturing subtle changes in facial expressions over time.
                </p>
              </div>
            </div>
            <dl
              className="mt-10 space-y-8 text-base leading-7 lg:max-w-none"
              data-aos="fade-right"
            >
              {features.map((feature) => (
                <div key={feature.name} className="relative pl-9">
                  <dt className="inline font-semibold">
                    <feature.icon
                      className="absolute left-1 top-1 h-5 w-5"
                      aria-hidden="true"
                    />
                    {feature.name}
                  </dt>{" "}
                  <dd className="inline">{feature.description}</dd>
                </div>
              ))}
            </dl>
          </div>
        </div>
      </div>
    </div>
  );
}
