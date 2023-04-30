// Returns a random DNA base
const returnRandBase = () => {
  const dnaBases = ['A', 'T', 'C', 'G'];
  return dnaBases[Math.floor(Math.random() * 4)];
};

// Returns a random single stand of DNA containing 15 bases
const mockUpStrand = () => {
  const newStrand = [];
  for (let i = 0; i < 15; i++) {
    newStrand.push(returnRandBase());
  }
  return newStrand;
};

// Returns a complementary DNA base
const returnComplementBase = base => {
  switch (base) {
    case 'A':
      return 'T';
      break;
    case 'T':
      return 'A';
      break;
    case 'C':
      return 'G;'
      break;
    case 'G':
      return 'C';
      break;
    default:
      console.log('Please enter a valid DNA base');
      break;
  }
};

const pAequorFactory = (num, dnaArray) => {
  return {
    specimenNum: num,
    dna: dnaArray,
    mutate() {
      const randIndex = Math.floor(Math.random() * this.dna.length);
      const originalBase = this.dna[randIndex];
      let newBase;
      do {
        newBase = returnRandBase();
        this.dna[randIndex] = newBase;
      } while (newBase === originalBase);
      return this.dna;
    },
    compareDNA (pAequorObject) {
      let identicalBases = 0;
      for (let i = 0; i < this.dna.length; i++) {
        if (this.dna[i] === pAequorObject.dna[i]) {
          identicalBases++;
        }
      }
      console.log(`specimen #${this.specimenNum} and specimen #${pAequorObject.specimenNum} have ${(identicalBases / 15)*100}% DNA in common`);
    },
    willLikelySurvive () {
      let basesCOrG = 0;
      this.dna.forEach(base => base === 'C' || base === 'G' ? basesCOrG++ : basesCOrG += 0);
      return basesCOrG / 15 >= 0.6 ? true : false;
    },
    complementStrand () {
      const complementaryStrand = this.dna.map(base => returnComplementBase(base));
      return complementaryStrand;
    }
  }
};

const pAequorArray = [];
for (let i = 1; i <= 30; i++) {
  const pAequorInstance = pAequorFactory(i, mockUpStrand());
  if (pAequorInstance.willLikelySurvive()) {
    pAequorArray.push(pAequorInstance);
  }
}

let commonPercent;
for (let i = 0; i < pAequorArray.length; i++) {
  for (let k = i + 1; k < pAequorArray.length; k++) {
    pAequorArray[i].compareDNA(pAequorArray[k]);
  }
}
