import { useState, useEffect } from "react";
import axios from "axios";
import "bulma/css/bulma.min.css";
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
    <div className="has-text-centered mt-5">
      <h1 className="title is-2 mb-4">Willkommen zum Schweiz-Quiz!</h1>
      <div className="field mb-4">
        <div className="control">
          <input
            type="text"
            placeholder="Gib deinen Namen ein"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="input"
          />
        </div>
      </div>
      <button onClick={startQuiz} className="button is-primary">
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
  const [incorrectAnswers, setIncorrectAnswers] = useState({});
  const [score, setScore] = useState(0);
  const [time, setTime] = useState(0);
  const [questionCount, setQuestionCount] = useState(0);
  const playerName = location.state?.name || "Anonym";
  const [startTime, setStartTime] = useState(null);

  useEffect(() => {
    setStartTime(Date.now());
    fetchQuestion();
  }, []);

  useEffect(() => {
    if (startTime) {
      const interval = setInterval(() => {
        setTime(((Date.now() - startTime) / 1000).toFixed(2));
      }, 1000);
      return () => clearInterval(interval);
    }
  }, [startTime]);

  const fetchQuestion = async () => {
    if (questionCount >= 5) {
      finishQuiz();
      return;
    }
    try {
      const response = await axios.get("http://localhost:5000/api/question");
      setQuestion(response.data);
      setSelectedAnswer(null);
      setFeedback("");
      setIncorrectAnswers({});
      setQuestionCount(questionCount + 1);
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
      setIncorrectAnswers(response.data.incorrect_answers || {});
      if (response.data.correct) {
        setScore(score + 1);
      }
      setTimeout(fetchQuestion, 3000);
    } catch (error) {
      console.error("Fehler bei der Antwortverarbeitung", error);
    }
  };

  const finishQuiz = () => {
    navigate("/results", { state: { score, time, name: playerName } });
  };

  if (!question) return <h3 className="has-text-centered mt-5">Lädt...</h3>;

  return (
    <div className="container has-text-centered mt-5">
      <h2 className="title is-4 mb-4">{question.text}</h2>
      <div className="buttons is-centered mb-4">
        {question.options.map((option, index) => (
          <button
            key={index}
            onClick={() => handleAnswer(option)}
            className="button is-light is-medium"
          >
            {option}
          </button>
        ))}
      </div>
      {feedback && <p className="has-text-weight-bold">{feedback}</p>}
      {Object.keys(incorrectAnswers).length > 0 && (
        <div className="mt-4">
          <h3 className="title is-5">Falsche Antworten:</h3>
          <ul>
            {Object.entries(incorrectAnswers).map(([city, value], idx) => (
              <li key={idx}>
                {city}: {value}
              </li>
            ))}
          </ul>
        </div>
      )}
      <p className="mt-4">Zeit: {time} Sekunden</p>
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
    <div className="container has-text-centered mt-5">
      <h2 className="title is-2 mb-4">Ergebnis</h2>
      <p>Name: {name}</p>
      <p>Punkte: {score}/5</p>
      <p>Zeit: {time} Sekunden</p>
      <h3 className="title is-4 mt-4">Top 3 Spieler</h3>
      <ul>
        {leaderboard.map((player, index) => (
          <li key={index}>
            {player.name}: {player.score} Punkte
          </li>
        ))}
      </ul>
      <Link to="/" className="button is-primary mt-4">
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
