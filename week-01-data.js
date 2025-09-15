const weekData = {
  week: 1,
  subHeader: "The first scores are in, the power rankings are set, and the waiver wire was buzzing.",
  footerText: "Good luck in Week 2. Try not to suck.",
  standings: [
    { rank: 1, teamName: "healzyswarriors", W: 1, L: 0, PF: 108.62 },
    { rank: 2, teamName: "FattyC26", W: 1, L: 0, PF: 97.92 },
    { rank: 3, teamName: "MorgsLev13", W: 1, L: 0, PF: 95.54 },
    { rank: 4, teamName: "coopersallstarz", W: 1, L: 0, PF: 93.72 },
    { rank: 5, teamName: "Stampy", W: 1, L: 0, PF: 92.06 },
    { rank: 6, teamName: "3whits", W: 1, L: 0, PF: 88.16 },
    { rank: 7, teamName: "webbyt", W: 1, L: 0, PF: 75.52 },
    { rank: 8, teamName: "Wicka", W: 1, L: 0, PF: 75.00 },
    { rank: 9, teamName: "5yearRebuild", W: 0, L: 1, PF: 91.08 },
    { rank: 10, teamName: "Bonzo22", W: 0, L: 1, PF: 87.02 },
    { rank: 11, teamName: "Sedgy", W: 0, L: 1, PF: 85.08 },
    { rank: 12, teamName: "Poddy", W: 0, L: 1, PF: 84.82 },
    { rank: 13, teamName: "DaksDemons", W: 0, L: 1, PF: 81.68 },
    { rank: 14, teamName: "MickyMayn", W: 0, L: 1, PF: 68.12 },
    { rank: 15, teamName: "gunga36", W: 0, L: 1, PF: 60.82 },
    { rank: 16, teamName: "JewTeam", W: 0, L: 1, PF: 57.22 }
  ],
  powerRankings: [
    { rank: 1, teamName: "healzyswarriors", blurb: "Dominant Week 1 performance, posting the highest score by a wide margin. Clear title favourite." },
    { rank: 2, teamName: "5yearRebuild", blurb: "Unlucky loss despite a huge score. This roster is deep and dangerous. A paper tiger for now." },
    { rank: 3, teamName: "FattyC26", blurb: "Solid win, solid team. Nothing flashy, just gets the job done. A quiet contender emerges." },
    { rank: 4, teamName: "MorgsLev13", blurb: "Took care of business against a struggling opponent. The real tests are yet to come." }
  ],
  transactions: {
    waivers: [
      { teamName: "Sedgy", player: "Kyren Williams", amount: 15 },
      { teamName: "MickyMayn", player: "Puka Nacua", amount: 11 }
    ],
    freeAgents: [
        { teamName: "3whits", player: "Justice Hill" },
        { teamName: "Wicka", player: "Nico Collins" }
    ]
  },
  matchups: [
    {
      teams: [
        { name: "healzyswarriors", score: 108.62, result: 'W', bestPlayer: { name: "Tyreek Hill", score: 38.50 }, worstPlayer: { name: "Javonte Williams", score: 4.90 } },
        { name: "Sedgy", score: 85.08, result: 'L', bestPlayer: { name: "Brandon Aiyuk", score: 29.90 }, worstPlayer: { name: "Pat Freiermuth", score: 1.20 } }
      ],
      recap: {
        title: "An Absolute Massacre",
        brutalRecap: "Healzy's Warriors didn't just win; they made a statement. With Tyreek Hill going nuclear, this was over before it started. Sedgy's squad put up a respectable score, but 'respectable' doesn't win you championships. This was a public execution.",
        coachingGrade: "A+",
        luck: "Couldn't be saved"
      }
    },
    {
        teams: [
          { name: "FattyC26", score: 97.92, result: 'W', bestPlayer: { name: "Aaron Jones", score: 27.70 }, worstPlayer: { name: "Jahan Dotson", score: 2.50 } },
          { name: "5yearRebuild", score: 91.08, result: 'L', bestPlayer: { name: "CeeDee Lamb", score: 24.10 }, worstPlayer: { name: "Drake London", score: 0.00 } }
        ],
        recap: {
          title: "The Heartbreaker",
          brutalRecap: "The closest matchup of the week, and a brutal one for 5yearRebuild, who scored the 2nd highest points of the week and still lost. FattyC26 ekes out a win thanks to a monster game from Aaron Jones. Fantasy can be a cruel, cruel mistress.",
          coachingGrade: "B-",
          luck: "Hard Yakka"
        }
      }
  ]
};