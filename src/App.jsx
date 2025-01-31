import { useState, useEffect } from "react";
import axios from "axios";
import {
  BrowserRouter as Router,
  Route,
  Routes,
  Link,
  useNavigate,
  useLocation,
} from "react-router-dom";

function Home() {
  const [name, setName] = useState("");
  const navigate = useNavigate();

  const startQuiz = () => {
    if (name.trim()) {
      navigate("/quiz", { state: { name } });
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <h1 className="text-2xl font-bold mb-4">Willkommen zum Schweiz-Quiz!</h1>
      <input
        type="text"
        placeholder="Gib deinen Namen ein"
        value={name}
        onChange={(e) => setName(e.target.value)}
        className="border p-2 rounded mb-4"
      />
      <button
        onClick={startQuiz}
        className="bg-blue-500 text-white px-4 py-2 rounded"
      >
        Starten
      </button>
    </div>
  );
}

function Quiz() {
  const location = useLocation();
  const navigate = useNavigate();
  const [question, setQuestion] = useState(null);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [feedback, setFeedback] = useState("");
  const [score, setScore] = useState(0);
  const [time, setTime] = useState(0);
  const [startTime, setStartTime] = useState(null);
  const playerName = location.state?.name || "Anonym";

  useEffect(() => {
    fetchQuestion();
    setStartTime(Date.now());
  }, []);

  const fetchQuestion = async () => {
    try {
      const response = await axios.get("http://localhost:5000/api/question");
      setQuestion(response.data);
      setSelectedAnswer(null);
      setFeedback("");
    } catch (error) {
      console.error("Fehler beim Laden der Frage", error);
    }
  };

  const handleAnswer = async (answer) => {
    try {
      const response = await axios.post("http://localhost:5000/api/answer", {
        question_id: question._id,
        answer: answer,
        name: playerName,
      });
      setFeedback(response.data.message);
      if (response.data.correct) {
        setScore(score + 1);
      }
      setTimeout(fetchQuestion, 2000);
    } catch (error) {
      console.error("Fehler bei der Antwortverarbeitung", error);
    }
  };

  const finishQuiz = () => {
    setTime((Date.now() - startTime) / 1000);
    navigate("/results", { state: { score, time, name: playerName } });
  };

  if (!question) return <p>Lädt...</p>;

  return (
    <div className="flex flex-col items-center mt-10">
      <h2 className="text-xl font-bold mb-4">{question.text}</h2>
      <div className="grid grid-cols-1 gap-2">
        {question.options.map((option, index) => (
          <button
            key={index}
            onClick={() => handleAnswer(option)}
            className="bg-gray-200 px-4 py-2 rounded hover:bg-gray-400"
          >
            {option}
          </button>
        ))}
      </div>
      {feedback && <p className="mt-4 font-bold">{feedback}</p>}
      <button
        onClick={finishQuiz}
        className="mt-4 bg-red-500 text-white px-4 py-2 rounded"
      >
        Quiz beenden
      </button>
    </div>
  );
}

function Results() {
  const location = useLocation();
  const navigate = useNavigate();
  const { score, time, name } = location.state || {
    score: 0,
    time: 0,
    name: "Anonym",
  };
  const [leaderboard, setLeaderboard] = useState([]);

  useEffect(() => {
    fetchLeaderboard();
  }, []);

  const fetchLeaderboard = async () => {
    try {
      const response = await axios.get("http://localhost:5000/api/leaderboard");
      setLeaderboard(response.data);
    } catch (error) {
      console.error("Fehler beim Laden des Leaderboards", error);
    }
  };

  return (
    <div className="flex flex-col items-center mt-10">
      <h2 className="text-2xl font-bold">Ergebnis</h2>
      <p>Name: {name}</p>
      <p>Punkte: {score}</p>
      <p>Zeit: {time.toFixed(2)} Sekunden</p>
      <h3 className="text-xl font-bold mt-4">Top 3 Spieler</h3>
      <ul>
        {leaderboard.map((player, index) => (
          <li key={index}>
            {player.name}: {player.score} Punkte
          </li>
        ))}
      </ul>
      <Link to="/" className="mt-4 bg-blue-500 text-white px-4 py-2 rounded">
        Neues Quiz
      </Link>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/quiz" element={<Quiz />} />
        <Route path="/results" element={<Results />} />
      </Routes>
    </Router>
  );
}

export default App;
