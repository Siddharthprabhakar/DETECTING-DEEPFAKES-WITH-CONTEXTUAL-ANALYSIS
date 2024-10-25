import { useEffect } from "react";
import AOS from "aos";
import "aos/dist/aos.css";

export default function Contact() {
  useEffect(() => {
    AOS.init({ duration: 1000 });
  }, []);
  
  return (
    <div className="py-24 sm:py-32" id="contact">
      <div className="mx-auto max-w-7xl px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-xl leading-7">Who are we ?</h2>
          <p className="mt-2 text-4xl font-bold tracking-tight sm:text-6xl">
            About Us
          </p>
        </div>
        
        {/* Replace the form with your company information */}
        <div className="mt-16 max-w-xl mx-auto" data-aos="zoom-in">
          <p className="text-lg leading-7">
          We are Samit Fernandes, Ralph Pereira, and Jaden Franco, studying Computer Engineering at St. Francis Institute of Technology, Mumbai University. This is our 3rd Year 2nd Term Project, aimed at developing innovative solutions to real-world challenges in the field of computer engineering.
          </p>
          <p className="mt-4 text-lg leading-7">
            In the age of rampant deepfake technology, our mission is to protect truth and integrity in digital media. Our DeepFake Detection App empowers users to identify and combat the spread of deceptive content. By leveraging advanced algorithms, we aim to ensure transparency, accountability, and trustworthiness in online discourse.
          </p>
        </div>
      </div>
    </div>
  );
}
