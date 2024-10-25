import Hero from "../Component/MainPage/Hero";
import About from "../Component/MainPage/About";
import Features from "../Component/MainPage/Features";
import Projects from "../Component/MainPage/Projects";
import Contact from "../Component/MainPage/Contact";
import Footer from "../Component/MainPage/Footer";

export default function Home() {
  return (
    <div className="overflow-x-hidden">
      <Hero />
      <About />
      <Features />
      <Projects />
      <Contact />
      <Footer />
    </div>
  );
}
