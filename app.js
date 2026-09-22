/**
 * ====================================================================
 * VoiceOver Studio SO — Application Logic (TTS & Asset Asli Resampler)
 * ====================================================================
 */

// Global Application State
const state = {
  // Current Mode: 'tts' or 'asset'
  mode: 'tts',

  // Active Selected Character (for TTS)
  selectedCharacter: 'prof_gasing_mentor',
  selectedVoice: 'id-ID-ArdiNeural',
  selectedPitchStr: '+2Hz',
  selectedRateStr: '+8%',
  selectedVibe: 'semangat',

  // DSP Tuner Sliders
  pitchSemitones: 0.0,
  speedFactor: 1.0,
  bassGain: 0.0,
  trebleGain: 0.0,
  volumeGain: 1.0,

  // Active Loaded Audio Source
  activeAudioUrl: null,
  activeAudioTitle: 'Prof. Gasing (Mentor Masa Depan)',
  activeRelPath: null,
  isAudioLoaded: false,
  lastGeneratedText: null,
  lastGeneratedChar: null,

  // Audio Playback & DSP
  audioContext: null,
  audioElement: null,
  sourceNode: null,
  bassFilter: null,
  trebleFilter: null,
  gainNode: null,
  analyserNode: null,
  isPlaying: false,
  isPaused: false,
  isExplicitlyStopped: false,
  isLooping: false,
  animationFrameId: null,

  // Catalog Data
  catalog: {
    pujian_gasing: [],
    prof_gasing: [],
    blaze: [],
    karakter_lain: []
  },
  allAssets: [],
  currentCategoryFilter: 'all',
  searchQuery: '',
  currentlyPlayingCardId: null,

  // F5-TTS Indo Studio State
  f5Voices: [],
  selectedF5VoiceId: 'so_marcia',
  selectedF5Category: 'all',
  isF5Generating: false,
  isRecording: false,
  mediaRecorder: null,
  recordedAudioChunks: [],
  recordedAudioBlob: null,
  recordedAudioUrl: null,
  recordTimerInterval: null,
  recordSeconds: 0,
  recordAudioContext: null,
  recordAnalyser: null,
  recordAnimFrameId: null,
  recordStream: null,
  recordMicSource: null,
  previewAudio: null,
  previewBufferSource: null,
  previewScrubAnimId: null,
  isPreviewPlaying: false,
  recordedAudioBuffer: null,
  recordedPcmData: null,
  lastF5AudioUrl: null,
  lastF5Format: 'wav',
  preMicStream: null,
  preMicSource: null,
  preMicAnalyser: null,
  preMicAnimFrameId: null,
  selectedDeviceId: null,
  modalCloningType: 'trainer' // 'trainer' or 'custom'
};

// Character Presets Dictionary (Client Side Mirror)
const characterPresets = {
  prof_gasing_mentor: {
    name: 'Prof. Gasing (Mentor Masa Depan)',
    voice: 'id-ID-ArdiNeural',
    pitch: '+2Hz',
    rate: '+8%',
    vibe: 'semangat',
    semitones: 1.0,
    speed: 1.05
  },
  prof_gasing_anime: {
    name: 'Prof. Gasing (Anime Semangat)',
    voice: 'id-ID-ArdiNeural',
    pitch: '+10Hz',
    rate: '+22%',
    vibe: 'semangat',
    semitones: 3.5,
    speed: 1.2
  },
  prof_gasing_narasi: {
    name: 'Prof. Gasing (Narasi Bijak)',
    voice: 'id-ID-ArdiNeural',
    pitch: '-4Hz',
    rate: '-5%',
    vibe: 'puitis',
    semitones: -1.5,
    speed: 0.95
  },
  master_tutor: {
    name: 'Master Tutor GASING (Lirik Kanan)',
    voice: 'id-ID-ArdiNeural',
    pitch: '+3Hz',
    rate: '+6%',
    vibe: 'ceria',
    semitones: 1.5,
    speed: 1.05
  },
  ksatria_octagon: {
    name: 'Ksatria Octagon (Xander)',
    voice: 'id-ID-ArdiNeural',
    pitch: '+12Hz',
    rate: '+18%',
    vibe: 'semangat',
    semitones: 4.0,
    speed: 1.15
  },
  sang_ratu: {
    name: 'Sang Ratu Babilon',
    voice: 'id-ID-GadisNeural',
    pitch: '-3Hz',
    rate: '-5%',
    vibe: 'misterius',
    semitones: -1.0,
    speed: 0.95
  },
  blaze: {
    name: 'Blaze (Penguasa Antagonis)',
    voice: 'id-ID-ArdiNeural',
    pitch: '-12Hz',
    rate: '-8%',
    vibe: 'dramatis',
    semitones: -4.0,
    speed: 0.92
  },
  narator: {
    name: 'Narator Sinematik Babilon',
    voice: 'id-ID-ArdiNeural',
    pitch: '-6Hz',
    rate: '-2%',
    vibe: 'dramatis',
    semitones: -2.0,
    speed: 0.98
  },
  vo_anak_ceria: {
    name: '👶 Suara Anak (Kids Voice)',
    voice: 'id-ID-GadisNeural',
    pitch: '+16Hz',
    rate: '+12%',
    vibe: 'ceria',
    semitones: 4.5,
    speed: 1.12
  },
  vo_korporat_formal: {
    name: '🏢 Suara Korporat (Corporate Voice)',
    voice: 'id-ID-ArdiNeural',
    pitch: '-2Hz',
    rate: '+0%',
    vibe: 'formal',
    semitones: -0.8,
    speed: 1.0
  },
  vo_youtube_vlog: {
    name: '📹 Suara YouTube / Vlog',
    voice: 'id-ID-ArdiNeural',
    pitch: '+3Hz',
    rate: '+10%',
    vibe: 'santai',
    semitones: 1.2,
    speed: 1.1
  },
  vo_audiobook_kisah: {
    name: '📚 Suara Audiobook',
    voice: 'id-ID-GadisNeural',
    pitch: '-3Hz',
    rate: '-6%',
    vibe: 'imersif',
    semitones: -1.2,
    speed: 0.94
  },
  vo_iklan_komersial: {
    name: '🎧 Suara Iklan (Commercial Voice)',
    voice: 'id-ID-GadisNeural',
    pitch: '+6Hz',
    rate: '+15%',
    vibe: 'persuasif',
    semitones: 2.2,
    speed: 1.15
  },
  vo_motivator_pria: {
    name: '⚡ Suara Motivator Pria Energik',
    voice: 'id-ID-ArdiNeural',
    pitch: '+5Hz',
    rate: '+14%',
    vibe: 'semangat',
    semitones: 2.0,
    speed: 1.14
  }
};

// Preset Texts
const presetTexts = {
  babilon: 'Salam Ksatria Octagon yang cerdas dan pemberani! Kamu luar biasa... Mampu mengalahkan mutan-mutan utusan Blaze di level pertama. Selamat! Kamu telah mendapatkan fragmen Sacred Octagon yang pertama. Asyik kan, belajar matematika sambil bermain game?',
  lirikKanan: 'Anak-anak yang hebat! Mari kita pelajari trik cepat Penjumlahan Dua Angka dengan metode GASING! Perhatikan: 43 + 29. Pertama, jumlahkan puluhannya: 4 + 2 = 6. Eits, sebelum menulis 6... Lirik kanan! Perhatikan satuannya: 3 + 9 = 12. Karena 12 lebih dari 10, puluhannya kita tambah 1 menjadi 7! Gampang dan asyik, kan?',
  pujianCeria: 'Kasih We O We... WOW! Hebaaat sekali kamu! Jawabanmu sangat tepat dan luar biasa cepat! Tetap semangat menjadi juara matematika!',
  anakCeria: 'Halo teman-teman cerdas! Wah, lihat ini, robot antariksa kita sudah siap meluncur ke galaksi bintang matematika! Ayo kita berpetualang dan hitung mundur bareng-bareng ya: Tiga, dua, satu... Meluncur!',
  korporat: 'Selamat datang di profil inovasi berkelanjutan kami. Dengan mengedepankan integrasi teknologi digital dan integritas profesional, kami berdedikasi menciptakan solusi bernilai tambah bagi kemajuan ekosistem bisnis modern di Indonesia.',
  youtubeVlog: 'Halo guys, balik lagi di channel kita! Hari ini gua bener-bener excited banget, soalnya perangkat yang kemarin kita tunggu-tunggu akhirnya mendarat di studio. Penasaran performanya gimana? Yuk, langsung kita bahas tuntas dan jangan lupa subscribe ya!',
  audiobook: 'Di bawah hamparan langit senja yang temaram, langkah kakinya terhenti di depan gerbang kayu tua itu. Angin pegunungan berhembus perlahan, seolah membisikkan kembali kisah masa silam yang telah lama terlelap di antara gemerisik dedaunan.',
  iklanKomersial: 'Mau belanja hemat tanpa repot? Sekarang saatnya beralih ke cara baru yang serba cepat dan praktis! Dapatkan diskon spesial hingga tujuh puluh persen hanya hari ini. Yuk, buka aplikasinya dan klaim promomu sekarang juga!',
  motivatorPria: 'Luar biasa! Jangan pernah ragukan kehebatan yang ada di dalam dirimu! Setiap tetes keringat dan perjuanganmu hari ini sedang membentuk masa depan yang gemilang. Bangkit, melangkah maju dengan gagah berani, dan buktikan bahwa kamu adalah sang juara!'
};

// DOM Elements
const tabBtnTTS = document.getElementById('tabBtnTTS');
const tabBtnSoundboard = document.getElementById('tabBtnSoundboard');
const tabContentTTS = document.getElementById('tabContentTTS');
const tabContentSoundboard = document.getElementById('tabContentSoundboard');
const globalSearchInput = document.getElementById('globalSearchInput');
const soundboardSearchInput = document.getElementById('soundboardSearchInput');
const narrationInput = document.getElementById('narrationInput');
const charCountEl = document.getElementById('charCount');
const wordCountEl = document.getElementById('wordCount');
const estDurationEl = document.getElementById('estDuration');
const selectedCharBadge = document.getElementById('selectedCharBadge');
const vibeBadge = document.getElementById('vibeBadge');
const smartMatchBanner = document.getElementById('smartMatchBanner');
const smartMatchTitle = document.getElementById('smartMatchTitle');
const btnLoadSmartMatch = document.getElementById('btnLoadSmartMatch');
const btnGenerateTTS = document.getElementById('btnGenerateTTS');
const btnGenerateTTSText = document.getElementById('btnGenerateTTSText');

// Studio DSP Elements
const activeModeBadge = document.getElementById('activeModeBadge');
const currentAudioTitle = document.getElementById('currentAudioTitle');
const currentAudioDuration = document.getElementById('currentAudioDuration');
const timeCurrent = document.getElementById('timeCurrent');
const timeTotal = document.getElementById('timeTotal');
const seekSlider = document.getElementById('seekSlider');
const btnMainPlay = document.getElementById('btnMainPlay');
const btnMainStop = document.getElementById('btnMainStop');
const btnMainLoop = document.getElementById('btnMainLoop');
const mainPlayText = document.getElementById('mainPlayText');
const mainPlayIcon = document.getElementById('mainPlayIcon');
const playbackStatusText = document.getElementById('playbackStatusText');
const pitchSlider = document.getElementById('pitchSlider');
const pitchBadge = document.getElementById('pitchBadge');
const speedSlider = document.getElementById('speedSlider');
const speedBadge = document.getElementById('speedBadge');
const bassSlider = document.getElementById('bassSlider');
const bassBadge = document.getElementById('bassBadge');
const trebleSlider = document.getElementById('trebleSlider');
const trebleBadge = document.getElementById('trebleBadge');
const volumeSlider = document.getElementById('volumeSlider');
const volumeBadge = document.getElementById('volumeBadge');
const btnDownloadWav = document.getElementById('btnDownloadWav');
const downloadBtnText = document.getElementById('downloadBtnText');
const btnDownloadMp3 = document.getElementById('btnDownloadMp3');
const downloadMp3BtnText = document.getElementById('downloadMp3BtnText');
const visualizerCanvas = document.getElementById('visualizerCanvas');
const visualizerOverlay = document.getElementById('visualizerOverlay');
const soundboardGrid = document.getElementById('soundboardGrid');
const catalogFilteredCount = document.getElementById('catalogFilteredCount');

// F5-TTS Studio DOM Elements
const tabBtnF5 = document.getElementById('tabBtnF5');
const tabContentF5 = document.getElementById('tabContentF5');
const f5DeviceBadge = document.getElementById('f5DeviceBadge');
const btnAutoCloneMarcia = document.getElementById('btnAutoCloneMarcia');
const btnAutoCloneJohn = document.getElementById('btnAutoCloneJohn');
const btnAutoCloneProf = document.getElementById('btnAutoCloneProf');
const btnOpenVoiceRecorder = document.getElementById('btnOpenVoiceRecorder');
const btnOpenAudioUpload = document.getElementById('btnOpenAudioUpload');
const f5SelectedVoiceBadge = document.getElementById('f5SelectedVoiceBadge');
const f5VoiceGrid = document.getElementById('f5VoiceGrid');
const f5BilingualSwitch = document.getElementById('f5BilingualSwitch');
const f5NarrationInput = document.getElementById('f5NarrationInput');
const f5PronunciationPreviewBox = document.getElementById('f5PronunciationPreviewBox');
const f5PronunciationText = document.getElementById('f5PronunciationText');
const f5ChunkCountBadge = document.getElementById('f5ChunkCountBadge');
const f5CharCount = document.getElementById('f5CharCount');
const f5WordCount = document.getElementById('f5WordCount');
const f5EstDuration = document.getElementById('f5EstDuration');
const btnF5ClearText = document.getElementById('btnF5ClearText');
const f5OutputFormat = document.getElementById('f5OutputFormat');
const f5NfeSteps = document.getElementById('f5NfeSteps');
const f5SpeedSlider = document.getElementById('f5SpeedSlider');
const f5SpeedLabel = document.getElementById('f5SpeedLabel');
const btnGenerateF5TTS = document.getElementById('btnGenerateF5TTS');
const btnGenerateF5TTSText = document.getElementById('btnGenerateF5TTSText');
const f5GenerateIcon = document.getElementById('f5GenerateIcon');

// Proyek Video DOM Elements
const tabBtnVideoProject = document.getElementById('tabBtnVideoProject');
const tabContentVideoProject = document.getElementById('tabContentVideoProject');
const leftTabsContainer = document.getElementById('leftTabsContainer');
const rightTunerContainer = document.getElementById('rightTunerContainer');
const videoOriginal = document.getElementById('videoOriginal');
const videoDubbed = document.getElementById('videoDubbed');
const btnVoiceModeF5 = document.getElementById('btnVoiceModeF5');
const btnVoiceModeEdge = document.getElementById('btnVoiceModeEdge');
const dubbedBadge = document.getElementById('dubbedBadge');
const dubbedAudioTrackLabel = document.getElementById('dubbedAudioTrackLabel');
const downloadDubbedVideoBtn = document.getElementById('downloadDubbedVideoBtn');
const downloadDubbedAudioBtn = document.getElementById('downloadDubbedAudioBtn');
const btnDualPlay = document.getElementById('btnDualPlay');
const btnStopBoth = document.getElementById('btnStopBoth');
const videoProjectSegmentsContainer = document.getElementById('videoProjectSegmentsContainer');
const projectSelectDropdown = document.getElementById('projectSelectDropdown');
const activeProjectDurationBadge = document.getElementById('activeProjectDurationBadge');
const videoProjectSegmentsCount = document.getElementById('videoProjectSegmentsCount');
const videoProjectTitle = document.getElementById('videoProjectTitle');
const videoProjectSubtitle = document.getElementById('videoProjectSubtitle');
const originalVideoDurationText = document.getElementById('originalVideoDurationText');
const downloadOriginalVideoBtn = document.getElementById('downloadOriginalVideoBtn');
const videoProjectSegmentsHeading = document.getElementById('videoProjectSegmentsHeading');
const videoProjectTotalDurationText = document.getElementById('videoProjectTotalDurationText');

// Voice Recording & AT Trainer Modal Elements
const voiceRecordModal = document.getElementById('voiceRecordModal');
const btnCloseRecordModal = document.getElementById('btnCloseRecordModal');
const btnCancelRecordModal = document.getElementById('btnCancelRecordModal');
const modalTitle = document.getElementById('modalTitle');
const modeBtnTrainer = document.getElementById('modeBtnTrainer');
const modeBtnCustom = document.getElementById('modeBtnCustom');
const labelSpeakerName = document.getElementById('labelSpeakerName');
const inputSpeakerName = document.getElementById('inputSpeakerName');
const labelRegion = document.getElementById('labelRegion');
const inputRegion = document.getElementById('inputRegion');
const selectNarratorRole = document.getElementById('selectNarratorRole');
const selectGender = document.getElementById('selectGender');
const inputRefText = document.getElementById('inputRefText');
const btnSwitchCalibScript = document.getElementById('btnSwitchCalibScript');
const recordLed = document.getElementById('recordLed');
const recordStatusLabel = document.getElementById('recordStatusLabel');
const recordTimer = document.getElementById('recordTimer');
const recordWaveCanvas = document.getElementById('recordWaveCanvas');
const micLevelMeter = document.getElementById('micLevelMeter');
const btnToggleRecord = document.getElementById('btnToggleRecord');
const recordBtnDot = document.getElementById('recordBtnDot');
const btnToggleRecordText = document.getElementById('btnToggleRecordText');
const btnPlayRecordedSample = document.getElementById('btnPlayRecordedSample');
const playSampleIcon = document.getElementById('playSampleIcon');
const playSampleText = document.getElementById('playSampleText');
const btnResetRecord = document.getElementById('btnResetRecord');
const modalAudioFileInput = document.getElementById('modalAudioFileInput');
const btnTriggerFileSelect = document.getElementById('btnTriggerFileSelect');
const selectedFileNameDisplay = document.getElementById('selectedFileNameDisplay');
const btnSaveClonedVoice = document.getElementById('btnSaveClonedVoice');
let selectMicDevice = document.getElementById('selectMicDevice');
let btnRefreshMicDevices = document.getElementById('btnRefreshMicDevices');
let btnTestSpeakerChime = document.getElementById('btnTestSpeakerChime');
let micLiveActivityDot = document.getElementById('micLiveActivityDot');
let micLiveActivityText = document.getElementById('micLiveActivityText');
let micLiveLevelPct = document.getElementById('micLiveLevelPct');
let micPreLiveMeter = document.getElementById('micPreLiveMeter');
let micDeviceAdvice = document.getElementById('micDeviceAdvice');

// Trainer Calibration Scripts
const trainerCalibScripts = [
  "Halo adik-adik pintar! Hari ini kita akan belajar matematika gasing bersama, gampang, asyik, dan menyenangkan!",
  "Selamat datang di petualangan ilmu pengetahuan Sacred Octagon, mari kita selesaikan misi berhitung cepat dengan gemilang!",
  "Luar biasa! Jawaban kamu sangat tepat dan cerdas, pertahankan prestasimu untuk babak berikutnya!",
  "Salam hangat semuanya, saya pembimbing dan narator modul hitung GASING, mari kita mulai pelajaran hari ini."
];
let currentCalibScriptIdx = 0;

let currentMatchedAsset = null;
let f5PreviewDebounceTimer = null;

/**
 * Initialize Web Audio API DSP Graph
 */
function initWebAudio() {
  if (state.audioContext) return;

  const AudioContextClass = window.AudioContext || window.webkitAudioContext;
  state.audioContext = new AudioContextClass();

  state.audioElement = new Audio();
  state.audioElement.crossOrigin = 'anonymous';

  state.sourceNode = state.audioContext.createMediaElementSource(state.audioElement);

  // Equalizer: Bass (Lowshelf) & Treble (Highshelf)
  state.bassFilter = state.audioContext.createBiquadFilter();
  state.bassFilter.type = 'lowshelf';
  state.bassFilter.frequency.value = 120;
  state.bassFilter.gain.value = state.bassGain;

  state.trebleFilter = state.audioContext.createBiquadFilter();
  state.trebleFilter.type = 'highshelf';
  state.trebleFilter.frequency.value = 3500;
  state.trebleFilter.gain.value = state.trebleGain;

  // Master Gain Node
  state.gainNode = state.audioContext.createGain();
  state.gainNode.gain.value = state.volumeGain;

  // Analyser Node for Visualizer
  state.analyserNode = state.audioContext.createAnalyser();
  state.analyserNode.fftSize = 128;

  // Connect Audio Graph: Source -> Bass -> Treble -> Gain -> Analyser -> Destination
  state.sourceNode.connect(state.bassFilter);
  state.bassFilter.connect(state.trebleFilter);
  state.trebleFilter.connect(state.gainNode);
  state.gainNode.connect(state.analyserNode);
  state.analyserNode.connect(state.audioContext.destination);

  // Audio Element Events
  state.audioElement.addEventListener('timeupdate', updatePlaybackProgress);
  state.audioElement.addEventListener('ended', onPlaybackEnded);
  state.audioElement.addEventListener('pause', () => {
    if (!state.audioElement.ended && !state.isExplicitlyStopped) {
      state.isPlaying = false;
      state.isPaused = true;
      updatePlaybackUI('Dijeda');
    }
  });
}

/**
 * Apply DSP Tuner Parameters (Pitch & Speed) to Active Audio Element
 */
function applyDSPParameters() {
  if (!state.audioElement) return;

  // Set playbackRate according to speed factor and pitch shift semitones
  // Note: HTMLMediaElement playbackRate changes both speed & pitch.
  // Pitch factor: 2^(semitones/12)
  const pitchFactor = Math.pow(2, state.pitchSemitones / 12.0);
  const totalRate = Math.max(0.25, Math.min(4.0, state.speedFactor * pitchFactor));

  // If preservesPitch is true in browser, playbackRate only affects tempo.
  // If preservesPitch is false, playbackRate shifts pitch!
  // If user only adjusts speed, keep preservesPitch = true.
  // If user adjusts pitch, we allow pitch shifting via preservesPitch = false.
  if (Math.abs(state.pitchSemitones) > 0.1) {
    state.audioElement.preservesPitch = false;
    state.audioElement.playbackRate = totalRate;
  } else {
    state.audioElement.preservesPitch = true;
    state.audioElement.playbackRate = state.speedFactor;
  }

  // Apply Equalizer & Gain
  if (state.bassFilter) state.bassFilter.gain.value = state.bassGain;
  if (state.trebleFilter) state.trebleFilter.gain.value = state.trebleGain;
  if (state.gainNode) state.gainNode.gain.value = state.volumeGain;
}

/**
 * Fetch Audio Catalog from Backend / Local JSON
 */
async function loadCatalog() {
  try {
    let res = await fetch('/api/catalog');
    let data;
    if (res.ok) {
      data = await res.json();
      state.catalog = data.catalog;
    } else {
      // Fallback to static json
      res = await fetch('assets/audio_catalog.json');
      state.catalog = await res.json();
    }

    // Flatten all assets
    state.allAssets = [];
    Object.keys(state.catalog).forEach(cat => {
      state.catalog[cat].forEach(item => {
        state.allAssets.push({ ...item, categoryKey: cat });
      });
    });

    renderSoundboard();
  } catch (err) {
    console.warn('Gagal memuat katalog audio:', err);
    showToast('Katalog lokal sedang dimuat...', 'info');
  }
}

/**
 * Render Soundboard Cards Grid
 */
function renderSoundboard() {
  if (!soundboardGrid) return;

  let filtered = state.allAssets;

  // 1. Filter by category
  if (state.currentCategoryFilter !== 'all') {
    filtered = filtered.filter(item => item.categoryKey === state.currentCategoryFilter);
  }

  // 2. Filter by search query
  if (state.searchQuery.trim()) {
    const q = state.searchQuery.toLowerCase().trim();
    filtered = filtered.filter(item => 
      item.title.toLowerCase().includes(q) ||
      item.transcript.toLowerCase().includes(q) ||
      item.character.toLowerCase().includes(q) ||
      item.filename.toLowerCase().includes(q)
    );
  }

  catalogFilteredCount.textContent = `${filtered.length} Asset Ditampilkan`;

  if (filtered.length === 0) {
    soundboardGrid.innerHTML = `
      <div class="p-10 text-center text-slate-500 col-span-full">
        Tidak ditemukan asset dengan kata kunci "<strong>${escapeHtml(state.searchQuery)}</strong>".
      </div>
    `;
    return;
  }

  soundboardGrid.innerHTML = filtered.map(item => {
    const isPlaying = state.isPlaying && state.currentlyPlayingCardId === item.id;
    const isActiveInStudio = state.activeRelPath === item.rel_path;

    return `
      <div class="sound-card ${isPlaying ? 'playing' : ''} ${isActiveInStudio ? 'active-in-studio' : ''}" data-id="${item.id}" data-rel="${item.rel_path}">
        <div>
          <div class="flex items-start justify-between gap-2">
            <div>
              <span class="text-[10px] font-semibold text-indigo-400 uppercase tracking-wider block">
                ${escapeHtml(item.character)}
              </span>
              <h4 class="text-xs font-bold text-slate-100 mt-0.5">${escapeHtml(item.title)}</h4>
            </div>
            <span class="px-2 py-0.5 rounded text-[10px] font-mono font-medium bg-slate-800 text-slate-300 shrink-0">
              ${item.duration}s
            </span>
          </div>
          <p class="text-[11px] text-slate-400 mt-2 line-clamp-2 italic leading-relaxed">
            "${escapeHtml(item.transcript)}"
          </p>
        </div>

        <div class="flex items-center justify-between pt-2 border-t border-slate-800/80 mt-1">
          <button
            type="button"
            class="btn-play-card flex items-center space-x-1.5 px-3 py-1.5 rounded-lg ${isPlaying ? 'bg-emerald-600 text-white' : 'bg-slate-800 hover:bg-slate-700 text-slate-200'} text-xs font-semibold transition-all"
            data-rel="${item.rel_path}"
            data-title="${escapeHtml(item.title)}"
            data-id="${item.id}"
          >
            <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 24 24">
              ${isPlaying ? '<path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>' : '<path d="M8 5v14l11-7z"/>'}
            </svg>
            <span>${isPlaying ? 'Jeda' : 'Putar'}</span>
          </button>

          <button
            type="button"
            class="btn-load-studio flex items-center space-x-1 px-3 py-1.5 rounded-lg bg-indigo-600/20 hover:bg-indigo-600/30 text-indigo-300 hover:text-white border border-indigo-500/30 text-xs font-medium transition-all"
            data-rel="${item.rel_path}"
            data-title="${escapeHtml(item.title)}"
            data-id="${item.id}"
          >
            <span>🎛️</span>
            <span>Muat ke Studio</span>
          </button>
        </div>
      </div>
    `;
  }).join('');

  // Attach card click handlers
  soundboardGrid.querySelectorAll('.btn-play-card').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const rel = btn.getAttribute('data-rel');
      const title = btn.getAttribute('data-title');
      const id = btn.getAttribute('data-id');
      playCardAudio(rel, title, id);
    });
  });

  soundboardGrid.querySelectorAll('.btn-load-studio').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const rel = btn.getAttribute('data-rel');
      const title = btn.getAttribute('data-title');
      loadAssetIntoStudio(rel, title);
    });
  });
}

/**
 * Load an Original Audio Asset into the Studio DSP Tuner
 */
function loadAssetIntoStudio(relPath, title) {
  initWebAudio();
  state.mode = 'asset';
  state.activeRelPath = relPath;
  state.activeAudioUrl = relPath;
  state.activeAudioTitle = title;
  state.isAudioLoaded = true;

  // Update UI indicators
  currentAudioTitle.textContent = title;
  activeModeBadge.textContent = 'Asset Asli: ' + title;
  activeModeBadge.className = 'px-2.5 py-1 rounded-full text-[10px] font-mono font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30';

  // Load into audio element
  state.audioElement.src = relPath;
  state.audioElement.load();

  showToast(`Asset asli "${title}" dimuat ke Studio Tuner. Atur pitch & speed sekarang!`, 'success');
  renderSoundboard();
}

/**
 * Play an audio card directly from Soundboard
 */
function playCardAudio(relPath, title, cardId) {
  initWebAudio();

  if (state.isPlaying && state.currentlyPlayingCardId === cardId) {
    pausePlayback();
    return;
  }

  loadAssetIntoStudio(relPath, title);
  state.currentlyPlayingCardId = cardId;
  startPlayback();
}

/**
 * Check Smart Phrase Matching
 */
function checkSmartPhraseMatch(text) {
  if (!text || text.length < 3) {
    smartMatchBanner.classList.add('hidden');
    currentMatchedAsset = null;
    return;
  }

  const clean = text.toLowerCase();
  let match = null;

  // Match prominent original phrases
  if (clean.includes('wow') || clean.includes('w o w') || clean.includes('we o we')) {
    match = state.allAssets.find(a => a.id.includes('22_Kasih_We_o_We_WOW') || a.title.includes('Kasih W O W'));
  } else if (clean.includes('hebat sekali')) {
    match = state.allAssets.find(a => a.id.includes('16_HEBAT_SEKALI') || a.title.includes('Hebat Sekali'));
  } else if (clean.includes('hebat') || clean.includes('hebaaat')) {
    match = state.allAssets.find(a => a.id.includes('03_HEBAT') || a.title.includes('Hebat!'));
  } else if (clean.includes('mantap')) {
    match = state.allAssets.find(a => a.id.includes('02_MANTAP') || a.id.includes('20_Wess_MANTAP'));
  } else if (clean.includes('luar biasa')) {
    match = state.allAssets.find(a => a.id.includes('15_Kamu_LUAR_BIASA') || a.id.includes('25_LUAR_BIASA'));
  } else if (clean.includes('blaze')) {
    match = state.allAssets.find(a => a.categoryKey === 'blaze');
  }

  if (match) {
    currentMatchedAsset = match;
    smartMatchTitle.textContent = match.title;
    smartMatchBanner.classList.remove('hidden');
  } else {
    smartMatchBanner.classList.add('hidden');
    currentMatchedAsset = null;
  }
}

/**
 * Update Text Statistics (Words, Chars, Estimated Duration)
 */
function updateTextStats() {
  const text = narrationInput.value;
  const chars = text.length;
  const words = text.trim() === '' ? 0 : text.trim().split(/\s+/).length;

  charCountEl.textContent = chars.toLocaleString('id-ID');
  wordCountEl.textContent = words.toLocaleString('id-ID');

  const wpm = 135 * state.speedFactor;
  const secs = words > 0 ? Math.ceil((words / wpm) * 60) : 0;
  if (secs < 60) {
    estDurationEl.textContent = `~${secs} dtk`;
  } else {
    const mins = Math.floor(secs / 60);
    const remainderSecs = secs % 60;
    estDurationEl.textContent = `~${mins} mnt ${remainderSecs} dtk`;
  }

  checkSmartPhraseMatch(text);
}

/**
 * Audio Visualizer Canvas Rendering
 */
let canvasCtx = visualizerCanvas.getContext('2d');
let wavePhase = 0;

function initCanvas() {
  const dpr = window.devicePixelRatio || 1;
  const rect = visualizerCanvas.getBoundingClientRect();
  visualizerCanvas.width = rect.width * dpr;
  visualizerCanvas.height = rect.height * dpr;
  canvasCtx.scale(dpr, dpr);
}

function renderVisualizer() {
  const rect = visualizerCanvas.getBoundingClientRect();
  const width = rect.width;
  const height = rect.height;

  canvasCtx.clearRect(0, 0, width, height);

  // Background subtle midline
  canvasCtx.strokeStyle = 'rgba(30, 41, 59, 0.4)';
  canvasCtx.lineWidth = 1;
  canvasCtx.beginPath();
  canvasCtx.moveTo(0, height / 2);
  canvasCtx.lineTo(width, height / 2);
  canvasCtx.stroke();

  if (state.isPlaying && !state.isPaused) {
    wavePhase += 0.08 * state.speedFactor;

    // Get frequency data from AnalyserNode if connected
    let freqData = new Uint8Array(64);
    if (state.analyserNode) {
      state.analyserNode.getByteFrequencyData(freqData);
    }

    const bars = 48;
    const barWidth = width / bars;

    for (let i = 0; i < bars; i++) {
      let freqValue = (freqData[i] || 0) / 255.0;
      if (freqValue === 0) {
        // Fallback simulation wave if node data not yet populated
        freqValue = (Math.sin(i * 0.3 + wavePhase) * 0.4 + 0.5);
      }

      const barHeight = Math.max(4, freqValue * (height * 0.75) * state.volumeGain);
      const x = i * barWidth;
      const y = (height - barHeight) / 2;

      // Gradient color
      const grad = canvasCtx.createLinearGradient(0, y, 0, y + barHeight);
      if (state.mode === 'asset') {
        grad.addColorStop(0, '#34d399');
        grad.addColorStop(1, '#059669');
      } else {
        grad.addColorStop(0, '#a855f7');
        grad.addColorStop(1, '#4f46e5');
      }

      canvasCtx.fillStyle = grad;
      canvasCtx.beginPath();
      canvasCtx.roundRect(x + 1, y, Math.max(barWidth - 2, 2), barHeight, 3);
      canvasCtx.fill();
    }
  } else {
    // Ambient resting sine wave
    canvasCtx.strokeStyle = 'rgba(99, 102, 241, 0.3)';
    canvasCtx.lineWidth = 1.5;
    canvasCtx.beginPath();
    for (let x = 0; x < width; x += 4) {
      const y = height / 2 + Math.sin(x * 0.03 + wavePhase * 0.05) * 3;
      if (x === 0) canvasCtx.moveTo(x, y);
      else canvasCtx.lineTo(x, y);
    }
    canvasCtx.stroke();
  }

  state.animationFrameId = requestAnimationFrame(renderVisualizer);
}

/**
 * Playback Control Functions
 */
async function startPlayback() {
  initWebAudio();

  if (state.audioContext.state === 'suspended') {
    await state.audioContext.resume();
  }

  const currentText = narrationInput ? narrationInput.value.trim() : '';
  const textChanged = (currentText !== state.lastGeneratedText) || (state.selectedCharacter !== state.lastGeneratedChar);

  // If in TTS mode and either no audio is loaded or text/character has changed, auto-generate!
  if (state.mode === 'tts' && (!state.activeAudioUrl || textChanged)) {
    if (currentText) {
      await generateTTS();
      return;
    } else {
      showToast('Tuliskan naskah narasi terlebih dahulu!', 'warning');
      narrationInput.focus();
      return;
    }
  }

  if (!state.audioElement.src || state.audioElement.src === window.location.href) {
    if (state.activeAudioUrl) {
      state.audioElement.src = state.activeAudioUrl;
    } else if (currentText) {
      await generateTTS();
      return;
    } else {
      showToast('Pilih karakter atau asset asli terlebih dahulu!', 'warning');
      return;
    }
  }

  applyDSPParameters();

  try {
    await state.audioElement.play();
    state.isPlaying = true;
    state.isPaused = false;
    updatePlaybackUI('Sedang Memutar...');
    visualizerOverlay.classList.add('hidden');
    renderSoundboard();
  } catch (err) {
    console.error('Playback error:', err);
    showToast('Gagal memutar audio: ' + err.message, 'error');
  }
}

function pausePlayback() {
  if (state.audioElement) {
    state.audioElement.pause();
    state.isPlaying = false;
    state.isPaused = true;
    updatePlaybackUI('Dijeda');
    renderSoundboard();
  }
}

function stopPlayback() {
  if (state.audioElement) {
    state.isExplicitlyStopped = true;
    state.audioElement.pause();
    state.audioElement.currentTime = 0;
    state.isPlaying = false;
    state.isPaused = false;
    state.currentlyPlayingCardId = null;
    updatePlaybackUI('Standby');
    visualizerOverlay.classList.remove('hidden');
    renderSoundboard();
    setTimeout(() => { state.isExplicitlyStopped = false; }, 80);
  }
}

function updatePlaybackUI(status) {
  playbackStatusText.textContent = status;
  if (state.isPlaying) {
    mainPlayText.textContent = 'Jeda';
    mainPlayIcon.innerHTML = '<path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>';
    btnMainPlay.className = 'btn-primary bg-amber-600 hover:bg-amber-500 px-5 py-2.5 text-xs font-bold flex items-center space-x-2';
  } else {
    mainPlayText.textContent = 'Putar Suara';
    mainPlayIcon.innerHTML = '<path d="M8 5v14l11-7z"/>';
    btnMainPlay.className = 'btn-primary px-5 py-2.5 text-xs font-bold flex items-center space-x-2';
  }
}

function updatePlaybackProgress() {
  if (!state.audioElement) return;

  const current = state.audioElement.currentTime || 0;
  const total = state.audioElement.duration || 0;

  timeCurrent.textContent = formatTime(current);
  timeTotal.textContent = formatTime(total);

  if (total > 0) {
    seekSlider.value = (current / total) * 100;
  }
}

function onPlaybackEnded() {
  if (state.isLooping) {
    state.audioElement.currentTime = 0;
    state.audioElement.play();
  } else {
    stopPlayback();
  }
}

function formatTime(seconds) {
  if (isNaN(seconds) || seconds === Infinity) return '00:00';
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
}

/**
 * Generate TTS Audio via FastAPI backend
 */
async function generateTTS() {
  const text = narrationInput.value.trim();
  if (!text) {
    showToast('Tuliskan atau tempelkan naskah narasi terlebih dahulu!', 'warning');
    narrationInput.focus();
    return;
  }

  btnGenerateTTS.disabled = true;
  btnGenerateTTSText.textContent = 'Memproses Suara AI Neural...';
  
  // Also reflect loading state on Main Play Button
  btnMainPlay.disabled = true;
  mainPlayText.textContent = 'Memproses Suara...';
  mainPlayIcon.innerHTML = `
    <svg class="animate-spin -ml-1 mr-1 h-3.5 w-3.5 text-white" fill="none" viewBox="0 0 24 24">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
    </svg>
  `;
  playbackStatusText.textContent = 'Merender Vokal Neural...';
  showToast('Memproses audio dengan model Neural vokal karakter...', 'info');

  try {
    const payload = {
      text: text,
      character_id: state.selectedCharacter,
      voice: state.selectedVoice,
      pitch: state.selectedPitchStr,
      rate: state.selectedRateStr,
      volume: '+0%'
    };

    const res = await fetch('/api/tts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Gagal menghasilkan TTS');
    }

    const data = await res.json();

    initWebAudio();
    state.mode = 'tts';
    state.activeAudioUrl = data.audio_url;
    state.activeAudioTitle = `${data.character} — TTS AI`;
    state.activeRelPath = data.audio_url;
    state.isAudioLoaded = true;
    state.lastGeneratedText = text;
    state.lastGeneratedChar = state.selectedCharacter;

    // Load to player
    state.audioElement.src = data.audio_url;
    state.audioElement.load();

    currentAudioTitle.textContent = state.activeAudioTitle;
    activeModeBadge.textContent = 'AI TTS Aktif: ' + data.character;
    activeModeBadge.className = 'px-2.5 py-1 rounded-full text-[10px] font-mono font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30';

    showToast(`Suara AI "${data.character}" berhasil dibuat! Memutar...`, 'success');
    
    // Play immediately
    applyDSPParameters();
    await state.audioElement.play();
    state.isPlaying = true;
    state.isPaused = false;
    updatePlaybackUI('Sedang Memutar...');
    visualizerOverlay.classList.add('hidden');
    renderSoundboard();

  } catch (err) {
    console.error('TTS error:', err);
    showToast('Gagal memproses suara: ' + err.message, 'error');
    updatePlaybackUI('Standby');
  } finally {
    btnGenerateTTS.disabled = false;
    btnGenerateTTSText.textContent = 'Hasilkan Suara AI (Generate Audio)';
    btnMainPlay.disabled = false;
  }
}

/**
 * Download Processed WAV Audio File
 */
async function downloadProcessedWav() {
  if (!state.isAudioLoaded && !state.activeAudioUrl && !narrationInput.value.trim()) {
    showToast('Pilih asset asli atau hasilkan audio terlebih dahulu!', 'warning');
    return;
  }

  const originalBtnContent = btnDownloadWav.innerHTML;
  btnDownloadWav.disabled = true;
  downloadBtnText.textContent = 'Merender WAV 16-bit PCM...';

  try {
    // If working with an Original Asset, call backend FFmpeg DSP for studio master quality
    if (state.mode === 'asset' && state.activeRelPath) {
      const payload = {
        rel_path: state.activeRelPath,
        pitch_semitones: state.pitchSemitones,
        speed_factor: state.speedFactor,
        bass_gain: state.bassGain,
        treble_gain: state.trebleGain
      };

      const res = await fetch('/api/process-audio', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!res.ok) {
        throw new Error('Gagal memproses audio di server');
      }

      const data = await res.json();

      // Trigger download
      const a = document.createElement('a');
      a.href = data.audio_url;
      a.download = data.filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);

      showToast(`Berhasil mengunduh master WAV: ${data.filename}`, 'success');
    } else {
      // If in TTS mode, ensure we have the rendered WAV URL
      if (!state.activeAudioUrl) {
        await generateTTS();
      }

      if (state.activeAudioUrl) {
        const a = document.createElement('a');
        a.href = state.activeAudioUrl;
        a.download = `SO_Voiceover_${Date.now()}.wav`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        showToast('Berhasil mengunduh audio narasi WAV!', 'success');
      }
    }
  } catch (err) {
    console.error('Download error:', err);
    showToast('Gagal mengunduh WAV: ' + err.message, 'error');
  } finally {
    btnDownloadWav.disabled = false;
    btnDownloadWav.innerHTML = originalBtnContent;
  }
}

/**
 * Dual Download: MP3 (320 kbps High Quality)
 */
async function downloadProcessedMp3() {
  if (!state.isAudioLoaded && !state.activeAudioUrl && !narrationInput.value.trim()) {
    showToast('Pilih asset asli atau hasilkan audio terlebih dahulu!', 'warning');
    return;
  }

  const originalBtnContent = btnDownloadMp3.innerHTML;
  btnDownloadMp3.disabled = true;
  if (downloadMp3BtnText) downloadMp3BtnText.textContent = 'Merender MP3 320k...';

  try {
    if (state.mode === 'asset' && state.activeRelPath) {
      const payload = {
        rel_path: state.activeRelPath,
        pitch_semitones: state.pitchSemitones,
        speed_factor: state.speedFactor,
        bass_gain: state.bassGain,
        treble_gain: state.trebleGain,
        format: 'mp3'
      };

      const res = await fetch('/api/process-audio', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!res.ok) throw new Error('Gagal memproses MP3 di server');
      const data = await res.json();

      const a = document.createElement('a');
      a.href = data.audio_url;
      a.download = data.filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);

      showToast(`Berhasil mengunduh MP3: ${data.filename}`, 'success');
    } else if (state.activeAudioUrl) {
      // If active audio is already MP3, download directly
      if (state.activeAudioUrl.endsWith('.mp3')) {
        const a = document.createElement('a');
        a.href = state.activeAudioUrl;
        a.download = `SO_Narasi_${Date.now()}.mp3`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        showToast('Berhasil mengunduh audio MP3!', 'success');
      } else {
        // Convert active WAV to MP3
        const cleanRel = state.activeAudioUrl.replace(/^\/output\//, '').replace(/^\/assets\//, '');
        const payload = {
          rel_path: cleanRel,
          pitch_semitones: state.pitchSemitones,
          speed_factor: state.speedFactor,
          bass_gain: state.bassGain,
          treble_gain: state.trebleGain,
          format: 'mp3'
        };

        const res = await fetch('/api/process-audio', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        if (res.ok) {
          const data = await res.json();
          const a = document.createElement('a');
          a.href = data.audio_url;
          a.download = data.filename;
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
          showToast(`Berhasil mengunduh MP3 320kbps: ${data.filename}`, 'success');
        } else {
          // Direct fallback download
          const a = document.createElement('a');
          a.href = state.activeAudioUrl;
          a.download = `SO_Narasi_${Date.now()}.wav`;
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
        }
      }
    }
  } catch (err) {
    console.error('MP3 download error:', err);
    showToast('Gagal mengunduh MP3: ' + err.message, 'error');
  } finally {
    btnDownloadMp3.disabled = false;
    btnDownloadMp3.innerHTML = originalBtnContent;
  }
}

/**
 * Toast Notification System
 */
function showToast(message, type = 'info') {
  const container = document.getElementById('toastContainer');
  const toast = document.createElement('div');

  let borderStyle = 'border-indigo-500/40 bg-slate-900/95 text-indigo-200';
  let dotColor = 'bg-indigo-400';

  if (type === 'success') {
    borderStyle = 'border-emerald-500/40 bg-slate-900/95 text-emerald-200';
    dotColor = 'bg-emerald-400';
  } else if (type === 'warning') {
    borderStyle = 'border-amber-500/40 bg-slate-900/95 text-amber-200';
    dotColor = 'bg-amber-400';
  } else if (type === 'error') {
    borderStyle = 'border-rose-500/40 bg-slate-900/95 text-rose-200';
    dotColor = 'bg-rose-400';
  }

  toast.className = `pointer-events-auto flex items-center space-x-2.5 px-4 py-3 rounded-xl border ${borderStyle} shadow-2xl text-xs font-medium transform transition-all duration-300 translate-y-2 opacity-0 backdrop-blur-md`;
  toast.innerHTML = `
    <span class="w-2 h-2 rounded-full ${dotColor} animate-pulse shrink-0"></span>
    <span class="leading-snug">${escapeHtml(message)}</span>
  `;

  container.appendChild(toast);

  requestAnimationFrame(() => {
    toast.classList.remove('translate-y-2', 'opacity-0');
  });

  setTimeout(() => {
    toast.classList.add('translate-y-2', 'opacity-0');
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

function escapeHtml(str) {
  if (!str) return '';
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

// =========================================================================
// F5-TTS INDO STUDIO & VOICE CLONING MODULE
// =========================================================================

/**
 * Switch Navigation Tab (TTS, Soundboard, F5-TTS Studio)
 */
function switchTab(tabName) {
  state.activeTab = tabName;

  const standardActive = 'nav-tab active flex items-center space-x-2 px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold transition-all bg-indigo-600 text-white shadow-md shadow-indigo-600/30';
  const standardInactive = 'nav-tab flex items-center space-x-2 px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold text-slate-400 hover:text-slate-200 hover:bg-slate-800/60 transition-all';
  const f5Active = 'nav-tab active flex items-center space-x-2 px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold transition-all bg-gradient-to-r from-amber-500 to-orange-500 text-slate-950 shadow-md shadow-amber-500/30 font-bold border border-amber-400';
  const f5Inactive = 'nav-tab flex items-center space-x-2 px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold text-slate-300 hover:text-white hover:bg-slate-800/80 transition-all border border-amber-500/40 bg-gradient-to-r from-amber-500/15 via-orange-500/10 to-indigo-500/15 shadow-sm shadow-amber-500/10';
  const vpActive = 'nav-tab active flex items-center space-x-2 px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold transition-all bg-gradient-to-r from-purple-600 via-fuchsia-600 to-indigo-600 text-white shadow-md shadow-purple-600/40 font-bold border border-purple-400';
  const vpInactive = 'nav-tab flex items-center space-x-2 px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold text-slate-300 hover:text-white hover:bg-slate-800/80 transition-all border border-purple-500/40 bg-gradient-to-r from-purple-500/15 via-fuchsia-500/10 to-indigo-500/15 shadow-sm shadow-purple-500/10';

  if (tabName === 'videoproject') {
    if (tabBtnTTS) tabBtnTTS.className = standardInactive;
    if (tabBtnSoundboard) tabBtnSoundboard.className = standardInactive;
    if (tabBtnF5) tabBtnF5.className = f5Inactive;
    if (tabBtnVideoProject) tabBtnVideoProject.className = vpActive;

    if (tabContentTTS) tabContentTTS.classList.add('hidden');
    if (tabContentSoundboard) tabContentSoundboard.classList.add('hidden');
    if (tabContentF5) tabContentF5.classList.add('hidden');
    if (tabContentVideoProject) tabContentVideoProject.classList.remove('hidden');

    if (leftTabsContainer) {
      leftTabsContainer.classList.remove('lg:col-span-7');
      leftTabsContainer.classList.add('lg:col-span-12');
    }
    if (rightTunerContainer) rightTunerContainer.classList.add('hidden');

    loadVideoProjectData();
    window.location.hash = '#/proyek-video';
  } else {
    if (tabBtnVideoProject) tabBtnVideoProject.className = vpInactive;
    if (tabContentVideoProject) tabContentVideoProject.classList.add('hidden');

    if (leftTabsContainer) {
      leftTabsContainer.classList.remove('lg:col-span-12');
      leftTabsContainer.classList.add('lg:col-span-7');
    }
    if (rightTunerContainer) rightTunerContainer.classList.remove('hidden');

    if (tabName === 'tts') {
      if (tabBtnTTS) tabBtnTTS.className = standardActive;
      if (tabBtnSoundboard) tabBtnSoundboard.className = standardInactive;
      if (tabBtnF5) tabBtnF5.className = f5Inactive;
      if (tabContentTTS) tabContentTTS.classList.remove('hidden');
      if (tabContentSoundboard) tabContentSoundboard.classList.add('hidden');
      if (tabContentF5) tabContentF5.classList.add('hidden');
    } else if (tabName === 'soundboard') {
      if (tabBtnTTS) tabBtnTTS.className = standardInactive;
      if (tabBtnSoundboard) tabBtnSoundboard.className = standardActive;
      if (tabBtnF5) tabBtnF5.className = f5Inactive;
      if (tabContentSoundboard) tabContentSoundboard.classList.remove('hidden');
      if (tabContentTTS) tabContentTTS.classList.add('hidden');
      if (tabContentF5) tabContentF5.classList.add('hidden');
    } else if (tabName === 'f5') {
      if (tabBtnTTS) tabBtnTTS.className = standardInactive;
      if (tabBtnSoundboard) tabBtnSoundboard.className = standardInactive;
      if (tabBtnF5) tabBtnF5.className = f5Active;
      if (tabContentF5) tabContentF5.classList.remove('hidden');
      if (tabContentTTS) tabContentTTS.classList.add('hidden');
      if (tabContentSoundboard) tabContentSoundboard.classList.add('hidden');

      checkF5Status();
      loadF5Voices();
    }
  }
}

// Video Project State & Logic
const videoProjectState = {
  currentProjectId: 'sprint_03_z1l1_bilangan_54s',
  projectsCache: {},
  data: null,
  activeVoiceMode: 'f5',
  activeSegmentAudio: null
};

async function loadVideoProjectData(projectId = null) {
  const targetId = projectId || (projectSelectDropdown ? projectSelectDropdown.value : 'sprint_03_z1l1_bilangan_54s');
  videoProjectState.currentProjectId = targetId;

  try {
    if (videoProjectState.projectsCache[targetId]) {
      videoProjectState.data = videoProjectState.projectsCache[targetId];
    } else {
      const res = await fetch(`/api/video-project/info?id=${encodeURIComponent(targetId)}`);
      if (!res.ok) throw new Error('Data proyek video belum siap');
      const data = await res.json();
      videoProjectState.projectsCache[targetId] = data;
      videoProjectState.data = data;
    }

    const data = videoProjectState.data;
    if (!data) return;

    // Update Header and badges
    if (videoProjectTitle) videoProjectTitle.textContent = data.title || 'Proyek Video Dubbing';
    if (activeProjectDurationBadge) activeProjectDurationBadge.textContent = `${(data.duration_seconds || 0).toFixed(2)} Detik`;
    if (videoProjectSegmentsCount) videoProjectSegmentsCount.textContent = `${(data.segments || []).length} Segmen`;
    if (videoProjectSegmentsHeading) videoProjectSegmentsHeading.textContent = `Detail Sinkronisasi Gerakan Tulisan (${(data.segments || []).length} Segmen)`;
    if (videoProjectTotalDurationText) videoProjectTotalDurationText.textContent = `Total Durasi: ${(data.duration_seconds || 0).toFixed(2)} Detik`;
    if (originalVideoDurationText) originalVideoDurationText.textContent = `${(data.duration_seconds || 0).toFixed(2)}s`;

    if (videoProjectSubtitle) {
      if (targetId === 'sprint_03_z1l1_bilangan_54s') {
        videoProjectSubtitle.textContent = 'Sprint 03: Mengganti rekaman naskah pengajaran Tutor John dengan suara kloning Guru Marcia yang jernih dan bebas noise (Accelerated F5-TTS + Spectral Denoiser), disinkronkan tepat dengan kartu pola angka 6–10.';
      } else if (targetId === 'z5l1_tanya_marcia') {
        videoProjectSubtitle.textContent = 'Sprint 02: Dubbing Suara Guru Marcia — Disinkronkan presisi dengan animasi visual pembagian & perkalian matematika Sacred Octagon.';
      } else {
        videoProjectSubtitle.textContent = 'Sprint 01: Mengganti rekaman naskah pengajaran Prof. Yohanes Surya dengan suara kloning Guru Marcia (Trainer Marcia), disinkronkan tepat dengan gerakan tulisan tangan di papan tulis.';
      }
    }

    // Set video aspect ratio
    const isWidescreen = targetId === 'z5l1_tanya_marcia' || targetId === 'sprint_03_z1l1_bilangan_54s';
    const aspectClass = isWidescreen ? 'w-full aspect-[16/9] object-contain bg-slate-950' : 'w-full aspect-[4/3] object-contain bg-slate-950';

    if (videoOriginal && data.files) {
      videoOriginal.src = data.files.original_video;
      videoOriginal.className = aspectClass;
    }
    if (videoDubbed) {
      videoDubbed.className = aspectClass;
    }
    if (downloadOriginalVideoBtn && data.files) {
      downloadOriginalVideoBtn.href = data.files.original_video;
      downloadOriginalVideoBtn.download = `${targetId}_original.mp4`;
    }

    updateDubbedAssets();
    renderVideoProjectSegments();
  } catch (err) {
    console.error('Error loading video project:', err);
    if (typeof showToast === 'function') {
      showToast('Gagal memuat data proyek video: ' + err.message, 'error');
    }
  }
}

function updateDubbedAssets() {
  if (!videoProjectState.data || !videoProjectState.data.files) return;
  const isF5 = videoProjectState.activeVoiceMode === 'f5';
  const files = videoProjectState.data.files;
  const dubbedVideoSrc = isF5 ? files.dubbed_video_f5 : files.dubbed_video_edge;
  const dubbedAudioSrc = isF5 ? files.dubbed_audio_f5 : files.dubbed_audio_edge;
  const targetId = videoProjectState.currentProjectId;
  const videoFileName = isF5 ? `${targetId}_dubbed_marcia_f5.mp4` : `${targetId}_dubbed_marcia_edge.mp4`;
  const audioFileName = isF5 ? 'master_dubbing_f5.mp3' : 'master_dubbing_edge.mp3';

  if (videoDubbed && dubbedVideoSrc) {
    const curTime = videoDubbed.currentTime || 0;
    const isPlaying = !videoDubbed.paused;
    videoDubbed.src = dubbedVideoSrc;
    videoDubbed.currentTime = curTime;
    if (isPlaying) videoDubbed.play().catch(() => {});
  }

  if (dubbedBadge) {
    dubbedBadge.textContent = isF5 ? 'F5-TTS Clone' : 'Edge-TTS Studio';
    dubbedBadge.className = isF5 
      ? 'px-2 py-0.5 rounded-full text-[9px] font-bold bg-amber-500 text-slate-950 uppercase tracking-wider'
      : 'px-2 py-0.5 rounded-full text-[9px] font-bold bg-purple-500 text-white uppercase tracking-wider';
  }

  if (dubbedAudioTrackLabel) {
    dubbedAudioTrackLabel.textContent = audioFileName;
  }

  if (downloadDubbedVideoBtn && dubbedVideoSrc) {
    downloadDubbedVideoBtn.href = dubbedVideoSrc;
    downloadDubbedVideoBtn.download = videoFileName;
  }
  if (downloadDubbedAudioBtn && dubbedAudioSrc) {
    downloadDubbedAudioBtn.href = dubbedAudioSrc;
    downloadDubbedAudioBtn.download = `${targetId}_${audioFileName}`;
  }
}

function setVideoProjectVoiceMode(mode) {
  videoProjectState.activeVoiceMode = mode;
  const isF5 = mode === 'f5';

  if (btnVoiceModeF5 && btnVoiceModeEdge) {
    if (isF5) {
      btnVoiceModeF5.className = 'px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all bg-gradient-to-r from-amber-500 to-orange-500 text-slate-950 shadow-md shadow-amber-500/20 cursor-pointer';
      btnVoiceModeEdge.className = 'px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-400 hover:text-slate-200 transition-all cursor-pointer';
    } else {
      btnVoiceModeF5.className = 'px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-400 hover:text-slate-200 transition-all cursor-pointer';
      btnVoiceModeEdge.className = 'px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-md shadow-purple-600/20 cursor-pointer';
    }
  }

  updateDubbedAssets();
  renderVideoProjectSegments();
}

function renderVideoProjectSegments() {
  if (!videoProjectSegmentsContainer || !videoProjectState.data) return;
  const segments = videoProjectState.data.segments || [];
  const isF5 = videoProjectState.activeVoiceMode === 'f5';
  const originalCharLabel = videoProjectState.data.original_character || 'Naskah Asli';
  const dubbedCharLabel = videoProjectState.data.dubbed_character || 'Suara Guru Marcia (Sinkron)';

  videoProjectSegmentsContainer.innerHTML = segments.map(seg => {
    const audioUrl = isF5 ? seg.audio_f5 : seg.audio_edge;
    const dur = (seg.end - seg.start).toFixed(2);
    return `
      <div class="p-4 rounded-xl bg-slate-950/70 border border-slate-800/80 hover:border-purple-500/40 transition-all flex flex-col md:flex-row md:items-center justify-between gap-3 group">
        <div class="space-y-1.5 flex-1">
          <div class="flex flex-wrap items-center gap-2">
            <span class="w-6 h-6 rounded-md bg-purple-500/20 text-purple-300 flex items-center justify-center text-xs font-bold font-mono">
              ${seg.id}
            </span>
            <span class="px-2 py-0.5 rounded-md text-[11px] font-mono font-semibold bg-slate-900 border border-slate-700 text-slate-300">
              ⏱️ ${seg.start.toFixed(2)}s – ${seg.end.toFixed(2)}s (${dur}s)
            </span>
            <span class="text-xs text-amber-300/90 font-medium flex items-center space-x-1">
              <span>✏️</span>
              <span>${seg.visual}</span>
            </span>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs pt-1">
            <div class="bg-slate-900/50 p-2.5 rounded-lg border border-slate-800">
              <span class="text-[10px] uppercase font-bold text-slate-400 block mb-0.5">${originalCharLabel}:</span>
              <p class="text-slate-300 italic">"${seg.prof_text}"</p>
            </div>
            <div class="bg-purple-950/30 p-2.5 rounded-lg border border-purple-800/40">
              <span class="text-[10px] uppercase font-bold text-purple-300 block mb-0.5">${dubbedCharLabel}:</span>
              <p class="text-purple-200 font-medium">"${seg.marcia_text}"</p>
            </div>
          </div>
        </div>
        <div class="flex items-center space-x-2 shrink-0 self-end md:self-center">
          <button
            type="button"
            class="play-seg-btn px-3 py-1.5 rounded-lg bg-purple-600/20 hover:bg-purple-600/40 border border-purple-500/30 text-purple-200 text-xs font-semibold flex items-center space-x-1 transition-all cursor-pointer"
            data-audio="${audioUrl}"
          >
            <span>▶️</span>
            <span>Audio Segmen</span>
          </button>
          <button
            type="button"
            class="seek-video-btn px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold flex items-center space-x-1 transition-all cursor-pointer"
            data-time="${seg.start}"
          >
            <span>🎯</span>
            <span>Lompat Video</span>
          </button>
        </div>
      </div>
    `;
  }).join('');

  videoProjectSegmentsContainer.querySelectorAll('.play-seg-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const url = btn.getAttribute('data-audio');
      if (!url) return;
      if (videoProjectState.activeSegmentAudio) {
        videoProjectState.activeSegmentAudio.pause();
      }
      const audio = new Audio(url);
      videoProjectState.activeSegmentAudio = audio;
      audio.play();
      btn.innerHTML = '<span>🔊</span><span>Memutar...</span>';
      audio.onended = () => {
        btn.innerHTML = '<span>▶️</span><span>Audio Segmen</span>';
      };
    });
  });

  videoProjectSegmentsContainer.querySelectorAll('.seek-video-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const t = parseFloat(btn.getAttribute('data-time') || '0');
      if (videoDubbed) {
        videoDubbed.currentTime = t;
        videoDubbed.play();
      }
      if (videoOriginal) {
        videoOriginal.currentTime = t;
        videoOriginal.play();
      }
    });
  });
}

/**
 * Check F5 Engine & Model Status
 */
async function checkF5Status() {
  try {
    const res = await fetch('/api/f5/status');
    if (!res.ok) return;
    const data = await res.json();
    if (f5DeviceBadge) {
      const isMps = data.device === 'mps';
      f5DeviceBadge.textContent = isMps ? 'Apple Silicon (MPS GPU)' : (data.device ? data.device.toUpperCase() : 'Apple Silicon MPS');
    }
  } catch (err) {
    console.warn('F5 Status check error:', err);
  }
}

/**
 * Load Voice Profiles from backend
 */
async function loadF5Voices() {
  try {
    const res = await fetch('/api/f5/voices');
    if (!res.ok) throw new Error('Gagal memuat profil suara F5');
    const data = await res.json();
    state.f5Voices = data.voices || [];
    renderF5VoiceGrid();
  } catch (err) {
    console.error('loadF5Voices error:', err);
    if (f5VoiceGrid) {
      f5VoiceGrid.innerHTML = `<div class="p-4 text-center text-rose-400 text-xs col-span-full">Gagal memuat suara: ${escapeHtml(err.message)}</div>`;
    }
  }
}

/**
 * Render Dynamic Voice Cards Grid
 */
function renderF5VoiceGrid() {
  if (!f5VoiceGrid) return;
  const filtered = state.f5Voices.filter(v => {
    if (state.selectedF5Category === 'all') return true;
    return v.category === state.selectedF5Category;
  });

  if (filtered.length === 0) {
    f5VoiceGrid.innerHTML = `
      <div class="col-span-full p-6 text-center text-slate-500 text-xs">
        Belum ada model suara untuk kategori ini. Gunakan tombol Rekam Suara AT / Mandiri di atas untuk menambahkan!
      </div>
    `;
    return;
  }

  f5VoiceGrid.innerHTML = filtered.map(v => {
    const isSelected = v.id === state.selectedF5VoiceId;
    const activeBorder = isSelected ? 'active border-amber-500 ring-2 ring-amber-500/40 bg-amber-950/25' : 'border-slate-800/80 hover:border-slate-700 bg-slate-900/50';
    const avatar = v.avatar || (v.category === 'so_character' ? '⭐' : (v.gender === 'Wanita' ? '👩‍🏫' : '👨‍🏫'));
    const isDeletable = (v.category === 'custom' || v.category === 'trainer_gasing' || v.id.startsWith('voice_') || v.id.startsWith('at_')) && v.id !== 'so_marcia' && v.id !== 'prof_yosu_asli' && v.id !== 'at_john';
    
    // Audio preview button if reference audio exists
    const audioPreviewBtn = v.ref_audio ? `
      <button
        type="button"
        class="f5-preview-ref-btn p-1.5 rounded-lg bg-slate-800/80 text-slate-300 hover:text-amber-300 hover:bg-slate-700 transition-all shrink-0 cursor-pointer"
        title="Dengarkan Contoh Suara Referensi"
        data-ref="${escapeHtml(v.ref_audio)}"
        data-name="${escapeHtml(v.name)}"
      >
        <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
      </button>
    ` : '';

    // Delete voice button for custom & trainer voices
    const deleteBtn = isDeletable ? `
      <button
        type="button"
        class="f5-delete-voice-btn p-1.5 rounded-lg bg-rose-500/15 text-rose-400 hover:text-white hover:bg-rose-600 border border-rose-500/30 hover:border-rose-500 transition-all shrink-0 cursor-pointer shadow-sm"
        title="Hapus Model Suara Ini (Permanen)"
        data-voiceid="${escapeHtml(v.id)}"
        data-name="${escapeHtml(v.name)}"
      >
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
        </svg>
      </button>
    ` : '';

    return `
      <div
        class="f5-voice-card p-3 rounded-2xl border transition-all cursor-pointer flex items-center justify-between space-x-3 group relative ${activeBorder}"
        data-voiceid="${escapeHtml(v.id)}"
      >
        <div class="flex items-center space-x-3 truncate">
          <div class="f5-voice-avatar shrink-0 text-xl flex items-center justify-center bg-slate-800/90 rounded-xl border border-slate-700/60 w-11 h-11">
            ${avatar}
          </div>
          <div class="truncate">
            <div class="flex items-center space-x-1.5">
              <span class="text-xs font-bold text-slate-100 group-hover:text-amber-300 transition-colors truncate">
                ${escapeHtml(v.name)}
              </span>
              ${isSelected ? '<span class="w-2 h-2 rounded-full bg-amber-400 shrink-0"></span>' : ''}
            </div>
            <p class="text-[11px] text-amber-400/90 font-medium truncate mt-0.5">
              ${escapeHtml(v.role || v.description || 'Voice Model')}
            </p>
            ${v.region ? `<span class="inline-block text-[9px] text-slate-400 bg-slate-800/90 px-1.5 py-0.2 rounded mt-0.5">${escapeHtml(v.region)}</span>` : ''}
          </div>
        </div>
        <div class="flex items-center space-x-1.5 shrink-0">
          ${audioPreviewBtn}
          ${deleteBtn}
          <span class="f5-check-icon w-5 h-5 rounded-full ${isSelected ? 'bg-amber-400 text-slate-950' : 'border border-slate-700 text-transparent'} flex items-center justify-center text-[10px] font-bold">
            ✓
          </span>
        </div>
      </div>
    `;
  }).join('');

  // Wire card selection
  f5VoiceGrid.querySelectorAll('.f5-voice-card').forEach(card => {
    card.addEventListener('click', (e) => {
      if (e.target.closest('.f5-preview-ref-btn') || e.target.closest('.f5-delete-voice-btn')) return;
      const voiceId = card.getAttribute('data-voiceid');
      selectF5Voice(voiceId);
    });

    // Right-click support on voice card to delete
    card.addEventListener('contextmenu', (e) => {
      const delBtn = card.querySelector('.f5-delete-voice-btn');
      if (delBtn) {
        e.preventDefault();
        const voiceId = delBtn.getAttribute('data-voiceid');
        const name = delBtn.getAttribute('data-name');
        deleteF5Voice(voiceId, name);
      }
    });
  });

  // Wire preview audio buttons
  f5VoiceGrid.querySelectorAll('.f5-preview-ref-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const refUrl = btn.getAttribute('data-ref');
      const name = btn.getAttribute('data-name');
      if (refUrl) {
        loadAssetIntoStudio(refUrl, `Sampel Suara: ${name}`);
        startPlayback();
      }
    });
  });

  // Wire delete voice buttons
  f5VoiceGrid.querySelectorAll('.f5-delete-voice-btn').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.stopPropagation();
      const voiceId = btn.getAttribute('data-voiceid');
      const name = btn.getAttribute('data-name');
      await deleteF5Voice(voiceId, name);
    });
  });
}

/**
 * Delete a custom or trainer voice model
 */
async function deleteF5Voice(voiceId, name) {
  if (!voiceId) return;

  const confirmed = window.confirm(`Apakah Anda yakin ingin menghapus model suara "${name}"?\n\nProfil kloning dan file rekaman audio ini akan dihapus.`);
  if (!confirmed) return;

  try {
    const res = await fetch(`/api/f5/voices/${encodeURIComponent(voiceId)}`, {
      method: 'DELETE'
    });
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail || 'Gagal menghapus model suara.');
    }

    showToast(`🗑️ Model suara "${name}" berhasil dihapus.`, 'info');

    // If deleted voice was active, fallback to blaze_original
    if (state.selectedF5VoiceId === voiceId) {
      state.selectedF5VoiceId = 'blaze_original';
    }

    // Refresh voices list from server
    await loadF5Voices();
  } catch (err) {
    console.error('Delete voice error:', err);
    showToast('Gagal menghapus model suara: ' + err.message, 'error');
  }
}

/**
 * Select active F5 Voice
 */
function selectF5Voice(voiceId) {
  state.selectedF5VoiceId = voiceId;
  const voice = state.f5Voices.find(v => v.id === voiceId);
  if (voice && f5SelectedVoiceBadge) {
    f5SelectedVoiceBadge.textContent = `${voice.name} (${voice.role || 'Aktif'})`;
  }
  renderF5VoiceGrid();
}

/**
 * Live Pronunciation & Bilingual Preview
 */
function updateF5PronunciationPreview() {
  const text = f5NarrationInput ? f5NarrationInput.value.trim() : '';
  const charCount = text.length;
  const words = text ? text.split(/\s+/).filter(Boolean).length : 0;
  const estSeconds = Math.max(1, Math.round(words / 2.6));

  if (f5CharCount) f5CharCount.textContent = charCount;
  if (f5WordCount) f5WordCount.textContent = words;
  if (f5EstDuration) f5EstDuration.textContent = text ? `~${estSeconds} dtk` : '~0 dtk';

  if (!text) {
    if (f5PronunciationText) {
      f5PronunciationText.textContent = '(Ketik naskah untuk melihat pratinjau pelafalan otomatis)';
    }
    if (f5ChunkCountBadge) f5ChunkCountBadge.textContent = '0 Bagian Kalimat';
    return;
  }

  clearTimeout(f5PreviewDebounceTimer);
  f5PreviewDebounceTimer = setTimeout(async () => {
    try {
      const applyBilingual = f5BilingualSwitch ? f5BilingualSwitch.checked : true;
      const res = await fetch('/api/f5/preview-pronunciation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: text,
          apply_pronunciation: applyBilingual
        })
      });

      if (!res.ok) return;
      const data = await res.json();
      if (f5PronunciationText) {
        f5PronunciationText.textContent = data.normalized_preview || text;
      }
      if (f5ChunkCountBadge) {
        const count = (data.chunk_count !== undefined ? data.chunk_count : data.chunks_count) || 1;
        f5ChunkCountBadge.textContent = `${count} Bagian Kalimat`;
      }
    } catch (err) {
      console.warn('Pronunciation preview error:', err);
    }
  }, 250);
}

/**
 * Generate F5-TTS Cloned Audio
 */
async function generateF5TTS() {
  const text = f5NarrationInput ? f5NarrationInput.value.trim() : '';
  if (!text) {
    showToast('Ketik narasi naskah terlebih dahulu!', 'warning');
    if (f5NarrationInput) f5NarrationInput.focus();
    return;
  }

  if (state.isF5Generating) return;
  state.isF5Generating = true;

  const originalBtnHtml = btnGenerateF5TTS.innerHTML;
  btnGenerateF5TTS.disabled = true;
  btnGenerateF5TTS.className = 'w-full py-4 px-6 rounded-2xl bg-amber-600/80 text-slate-900 font-extrabold text-sm sm:text-base flex items-center justify-center space-x-3 shadow-lg cursor-not-allowed opacity-90';
  btnGenerateF5TTS.innerHTML = `
    <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-slate-950" fill="none" viewBox="0 0 24 24">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
    </svg>
    <span>Sedang Mengkloning Suara F5-TTS V2 (MPS Acceleration)...</span>
  `;

  try {
    const payload = {
      voice_id: state.selectedF5VoiceId || 'so_marcia',
      text: text,
      speed: f5SpeedSlider ? parseFloat(f5SpeedSlider.value) : 1.0,
      nfe_step: f5NfeSteps ? parseInt(f5NfeSteps.value, 10) : 32,
      output_format: f5OutputFormat ? f5OutputFormat.value : 'wav',
      apply_bilingual: f5BilingualSwitch ? f5BilingualSwitch.checked : true,
      apply_gasing: true
    };

    const res = await fetch('/api/f5/tts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.detail || 'Gagal menghasilkan audio kloning F5');
    }

    const data = await res.json();
    state.lastF5AudioUrl = data.audio_url;
    state.lastF5Format = data.format || 'wav';

    // Load into Studio Audio Tuner immediately
    const title = `${data.character_name || 'Kloning F5'} (${(data.format || 'wav').toUpperCase()})`;
    loadAssetIntoStudio(data.audio_url, title);
    startPlayback();

    showToast(`Kloning selesai dalam ${data.generation_time}s! Audio siap di Studio Tuner.`, 'success');
  } catch (err) {
    console.error('generateF5TTS error:', err);
    showToast('Error Kloning F5: ' + err.message, 'error');
  } finally {
    state.isF5Generating = false;
    btnGenerateF5TTS.disabled = false;
    btnGenerateF5TTS.className = 'w-full py-4 px-6 rounded-2xl bg-gradient-to-r from-amber-500 via-orange-500 to-amber-600 hover:from-amber-400 hover:to-orange-500 text-slate-950 font-extrabold text-sm sm:text-base flex items-center justify-center space-x-3 shadow-lg shadow-amber-500/25 transition-all transform hover:-translate-y-0.5 active:translate-y-0 cursor-pointer';
    btnGenerateF5TTS.innerHTML = originalBtnHtml;
  }
}

/**
 * Convert Float32Array PCM samples directly to 16-bit PCM WAV Blob
 */
function encodeFloat32ToWavBlob(samples, sampleRate) {
  const numChannels = 1;
  const bitDepth = 16;
  const bytesPerSample = bitDepth / 8;
  const blockAlign = numChannels * bytesPerSample;
  const dataLength = samples.length * bytesPerSample;
  const bufferLength = 44 + dataLength;
  const buffer = new ArrayBuffer(bufferLength);
  const view = new DataView(buffer);

  function writeString(offset, str) {
    for (let i = 0; i < str.length; i++) {
      view.setUint8(offset + i, str.charCodeAt(i));
    }
  }

  // RIFF Chunk
  writeString(0, 'RIFF');
  view.setUint32(4, 36 + dataLength, true);
  writeString(8, 'WAVE');

  // fmt Subchunk
  writeString(12, 'fmt ');
  view.setUint32(16, 16, true);
  view.setUint16(20, 1, true); // PCM format
  view.setUint16(22, numChannels, true);
  view.setUint32(24, sampleRate, true);
  view.setUint32(28, sampleRate * blockAlign, true);
  view.setUint16(32, blockAlign, true);
  view.setUint16(34, bitDepth, true);

  // data Subchunk
  writeString(36, 'data');
  view.setUint32(40, dataLength, true);

  // Write clamped 16-bit PCM samples
  let offset = 44;
  for (let i = 0; i < samples.length; i++, offset += 2) {
    let s = Math.max(-1, Math.min(1, samples[i]));
    view.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
  }

  return new Blob([view], { type: 'audio/wav' });
}

/**
 * Convert AudioBuffer to 16-bit PCM WAV Blob (Universal Cross-Browser Compatibility)
 */
function encodeAudioBufferToWav(audioBuffer) {
  const numChannels = 1;
  const sampleRate = audioBuffer.sampleRate;
  let samples;
  if (audioBuffer.numberOfChannels === 1) {
    samples = audioBuffer.getChannelData(0);
  } else {
    const ch0 = audioBuffer.getChannelData(0);
    const ch1 = audioBuffer.getChannelData(1);
    samples = new Float32Array(ch0.length);
    for (let i = 0; i < ch0.length; i++) {
      samples[i] = (ch0[i] + ch1[i]) * 0.5;
    }
  }
  return encodeFloat32ToWavBlob(samples, sampleRate);
}

/**
 * Render the static completed voice waveform of the recorded audio with amplitude peaks & playhead
 */
function drawRecordedWaveformSnapshot(progressPercent = 0) {
  if (!recordWaveCanvas) return;
  const ctx = recordWaveCanvas.getContext('2d');
  const w = recordWaveCanvas.width = recordWaveCanvas.offsetWidth || 400;
  const h = recordWaveCanvas.height = recordWaveCanvas.offsetHeight || 64;

  ctx.fillStyle = '#090d16';
  ctx.fillRect(0, 0, w, h);

  // Subtle center line
  ctx.strokeStyle = '#1e293b';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(0, h / 2);
  ctx.lineTo(w, h / 2);
  ctx.stroke();

  if (!state.recordedPcmData || state.recordedPcmData.length === 0) {
    // Standby idle wave line
    ctx.strokeStyle = '#334155';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    for (let x = 0; x < w; x++) {
      const y = h / 2 + Math.sin(x * 0.06) * 3.5;
      if (x === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();

    // Helper text
    ctx.fillStyle = '#64748b';
    ctx.font = '11px Inter, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('Klik "Mulai Merekam Suara" dan bacalah naskah kalibrasi', w / 2, h / 2 + 18);
    return;
  }

  const pcm = state.recordedPcmData;
  const numBars = Math.min(100, Math.floor(w / 3.4));
  const step = Math.floor(pcm.length / numBars);
  const barWidth = w / numBars;

  for (let i = 0; i < numBars; i++) {
    let max = 0;
    const start = i * step;
    for (let j = 0; j < step; j += 6) {
      const val = Math.abs(pcm[start + j] || 0);
      if (val > max) max = val;
    }

    const amp = Math.pow(max, 0.75);
    const barHeight = Math.max(3, Math.min(h - 10, amp * (h - 10) * 1.8));
    const x = i * barWidth;
    const y = (h - barHeight) / 2;

    const barProg = (i / numBars) * 100;
    const isPlayed = barProg <= progressPercent;

    if (isPlayed) {
      const grad = ctx.createLinearGradient(0, y, 0, y + barHeight);
      grad.addColorStop(0, '#34d399');
      grad.addColorStop(1, '#059669');
      ctx.fillStyle = grad;
    } else {
      const grad = ctx.createLinearGradient(0, y, 0, y + barHeight);
      grad.addColorStop(0, '#fbbf24');
      grad.addColorStop(1, '#ea580c');
      ctx.fillStyle = grad;
    }

    ctx.fillRect(x + 0.5, y, Math.max(1.5, barWidth - 1), barHeight);
  }

  // Draw playhead cursor if playing
  if (progressPercent > 0 && progressPercent < 100) {
    const playheadX = (progressPercent / 100) * w;
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 2.5;
    ctx.shadowColor = '#10b981';
    ctx.shadowBlur = 10;
    ctx.beginPath();
    ctx.moveTo(playheadX, 2);
    ctx.lineTo(playheadX, h - 2);
    ctx.stroke();
    ctx.shadowBlur = 0;
  }
}

/**
 * Stop any ongoing preview playback of recorded audio
 */
function stopRecordedSamplePlayback() {
  if (state.previewAudio) {
    state.previewAudio.pause();
    state.previewAudio = null;
  }
  if (state.previewBufferSource) {
    try { state.previewBufferSource.stop(); } catch (e) {}
    state.previewBufferSource = null;
  }
  if (state.previewScrubAnimId) {
    cancelAnimationFrame(state.previewScrubAnimId);
    state.previewScrubAnimId = null;
  }
  state.isPreviewPlaying = false;
  const dur = state.recordSeconds || 1;
  if (playSampleIcon) playSampleIcon.textContent = '▶';
  if (playSampleText) playSampleText.textContent = `Putar Hasil Rekaman (${dur} dtk)`;
  if (btnPlayRecordedSample) btnPlayRecordedSample.classList.remove('play-sample-playing');
  drawRecordedWaveformSnapshot(0);
}

/**
 * Reset Recording State and UI
 */
function resetRecordingState() {
  stopRecordedSamplePlayback();

  if (state.recordStream) {
    state.recordStream.getTracks().forEach(t => t.stop());
    state.recordStream = null;
  }
  if (state.recordMicSource) {
    try { state.recordMicSource.disconnect(); } catch (e) {}
    state.recordMicSource = null;
  }
  if (state.mediaRecorder && state.mediaRecorder.state !== 'inactive') {
    try { state.mediaRecorder.stop(); } catch (e) {}
  }

  state.isRecording = false;
  state.recordedAudioChunks = [];
  state.recordedPcmData = null;
  state.recordedAudioBuffer = null;
  if (state.recordedAudioUrl) {
    URL.revokeObjectURL(state.recordedAudioUrl);
    state.recordedAudioUrl = null;
  }
  state.recordedAudioBlob = null;
  state.recordSeconds = 0;

  clearInterval(state.recordTimerInterval);
  cancelAnimationFrame(state.recordAnimFrameId);

  if (recordTimer) recordTimer.textContent = '00:00';
  if (recordStatusLabel) recordStatusLabel.textContent = 'Mikrofon Standby — Siap Merekam';
  if (recordLed) recordLed.className = 'w-2.5 h-2.5 rounded-full bg-slate-600 transition-colors';
  if (micLevelMeter) micLevelMeter.style.width = '0%';

  // Show Record button in standby
  if (btnToggleRecord) {
    btnToggleRecord.classList.remove('hidden', 'recording-active-btn');
    btnToggleRecord.className = 'py-2.5 px-5 rounded-xl bg-rose-600 hover:bg-rose-500 text-white text-xs font-bold flex items-center space-x-2 shadow-lg shadow-rose-600/25 transition-all cursor-pointer';
    if (recordBtnDot) recordBtnDot.className = 'w-3 h-3 rounded-full bg-white';
    if (btnToggleRecordText) btnToggleRecordText.textContent = 'Mulai Merekam Suara';
  }

  // Hide Play button & Reset button until recorded
  if (btnPlayRecordedSample) {
    btnPlayRecordedSample.classList.add('hidden');
    btnPlayRecordedSample.disabled = true;
    btnPlayRecordedSample.classList.remove('play-sample-active', 'play-sample-playing');
    if (playSampleIcon) playSampleIcon.textContent = '▶';
    if (playSampleText) playSampleText.textContent = 'Putar Hasil Rekaman';
  }

  if (btnResetRecord) btnResetRecord.classList.add('hidden');
  if (btnSaveClonedVoice) btnSaveClonedVoice.disabled = true;
  if (selectedFileNameDisplay) selectedFileNameDisplay.textContent = '';
  if (modalAudioFileInput) modalAudioFileInput.value = '';

  updateModalFooterStatus('Belum ada audio', 'idle');
  drawRecordedWaveformSnapshot(0);
}

/**
 * Update Status Indicator in Modal Sticky Footer
 */
function updateModalFooterStatus(statusText, type = 'idle') {
  const indicator = document.getElementById('footerSampleIndicator');
  const statusEl = document.getElementById('footerSampleStatus');
  if (!statusEl) return;
  
  statusEl.textContent = statusText;
  if (!indicator) return;

  if (type === 'success') {
    indicator.className = 'w-2 h-2 rounded-full bg-emerald-400 shadow-sm shadow-emerald-400';
    statusEl.className = 'font-medium text-emerald-300';
  } else if (type === 'recording') {
    indicator.className = 'w-2 h-2 rounded-full bg-rose-500 animate-pulse shadow-sm shadow-rose-500';
    statusEl.className = 'font-medium text-rose-300';
  } else if (type === 'warning') {
    indicator.className = 'w-2 h-2 rounded-full bg-amber-400 shadow-sm shadow-amber-400';
    statusEl.className = 'font-medium text-amber-300';
  } else {
    indicator.className = 'w-2 h-2 rounded-full bg-slate-600';
    statusEl.className = 'font-medium text-slate-400';
  }
}

/**
 * Ensure Microphone Selector and Sound Check UI is present in DOM
 */
function ensureMicSelectorInDOM() {
  selectMicDevice = document.getElementById('selectMicDevice');
  btnRefreshMicDevices = document.getElementById('btnRefreshMicDevices');
  btnTestSpeakerChime = document.getElementById('btnTestSpeakerChime');
  micLiveActivityDot = document.getElementById('micLiveActivityDot');
  micLiveActivityText = document.getElementById('micLiveActivityText');
  micLiveLevelPct = document.getElementById('micLiveLevelPct');
  micPreLiveMeter = document.getElementById('micPreLiveMeter');
  micDeviceAdvice = document.getElementById('micDeviceAdvice');

  if (selectMicDevice) return;

  const modal = document.getElementById('voiceRecordModal');
  if (!modal) return;

  const modalContainer = document.getElementById('modalBodyScrollable') || 
                         modal.querySelector('.modal-scroll-area') || 
                         modal.querySelector('.overflow-y-auto') || 
                         modal.querySelector('.space-y-4');
  if (!modalContainer) return;

  const recordWaveCanvas = document.getElementById('recordWaveCanvas');
  const recordBox = recordWaveCanvas ? (recordWaveCanvas.closest('.space-y-3') || recordWaveCanvas.closest('.space-y-2\\.5') || recordWaveCanvas.parentElement.parentElement) : null;

  const micSection = document.createElement('div');
  micSection.id = 'micSelectorWrapper';
  micSection.className = 'p-3 rounded-xl bg-slate-900/90 border border-slate-800 space-y-2';
  micSection.innerHTML = `
    <div class="flex items-center justify-between">
      <label for="selectMicDevice" class="text-[11px] font-semibold text-slate-300 flex items-center space-x-1.5">
        <span>🎙️</span>
        <span>Pilih Sumber Mikrofon:</span>
      </label>
      <button
        type="button"
        id="btnTestSpeakerChime"
        class="text-[10px] text-indigo-400 hover:text-indigo-300 font-medium px-2 py-0.5 rounded-lg bg-indigo-500/10 border border-indigo-500/20 transition-all flex items-center space-x-1 cursor-pointer"
        title="Uji apakah speaker/audio komputer Anda aktif"
      >
        <span>🔊</span>
        <span>Tes Audio Speaker</span>
      </button>
    </div>
    <div class="flex items-center space-x-2">
      <select
        id="selectMicDevice"
        class="flex-1 bg-slate-950 border border-slate-700/80 rounded-lg px-2.5 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-amber-400 cursor-pointer"
      >
        <option value="">Memuat daftar mikrofon...</option>
      </select>
      <button
        type="button"
        id="btnRefreshMicDevices"
        class="px-2.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs border border-slate-700 transition-all cursor-pointer"
        title="Segarkan daftar mikrofon"
      >
        🔄
      </button>
    </div>

    <!-- Live Pre-Recording Mic Level & Activity Indicator -->
    <div class="flex items-center justify-between text-[11px] pt-1">
      <span class="text-slate-400 flex items-center space-x-1">
        <span id="micLiveActivityDot" class="w-2 h-2 rounded-full bg-slate-600 transition-colors"></span>
        <span id="micLiveActivityText">Level Suara Mikrofon:</span>
      </span>
      <span id="micLiveLevelPct" class="font-mono text-emerald-400 font-bold">0%</span>
    </div>
    <div class="w-full h-1.5 rounded-full bg-slate-800 overflow-hidden">
      <div id="micPreLiveMeter" class="h-full bg-gradient-to-r from-emerald-500 via-amber-400 to-rose-500 w-0 transition-all duration-75"></div>
    </div>
    <p id="micDeviceAdvice" class="text-[10px] text-slate-400 leading-tight">
      💡 Tips: Berbicaralah sekarang. Jika meteran di atas tidak bergerak hijau, silakan ganti pilihan mikrofon ke <b>MacBook Pro Microphone</b> atau <b>YS Microphone</b>.
    </p>
  `;

  if (recordBox && recordBox.parentNode) {
    recordBox.parentNode.insertBefore(micSection, recordBox);
  } else {
    modalContainer.appendChild(micSection);
  }

  selectMicDevice = document.getElementById('selectMicDevice');
  btnRefreshMicDevices = document.getElementById('btnRefreshMicDevices');
  btnTestSpeakerChime = document.getElementById('btnTestSpeakerChime');
  micLiveActivityDot = document.getElementById('micLiveActivityDot');
  micLiveActivityText = document.getElementById('micLiveActivityText');
  micLiveLevelPct = document.getElementById('micLiveLevelPct');
  micPreLiveMeter = document.getElementById('micPreLiveMeter');
  micDeviceAdvice = document.getElementById('micDeviceAdvice');

  if (btnTestSpeakerChime) btnTestSpeakerChime.addEventListener('click', playTestSpeakerChime);
  if (btnRefreshMicDevices) {
    btnRefreshMicDevices.addEventListener('click', async () => {
      await populateMicDevices();
      showToast('Daftar mikrofon diperbarui.', 'info');
    });
  }
  if (selectMicDevice) {
    selectMicDevice.addEventListener('change', (e) => {
      state.selectedDeviceId = e.target.value;
      startPreMicMonitoring(e.target.value);
    });
  }
}

/**
 * Populate Available Audio Input Devices (Microphones)
 */
async function populateMicDevices() {
  ensureMicSelectorInDOM();
  if (!selectMicDevice) return;
  selectMicDevice.innerHTML = '<option value="">Memindai mikrofon...</option>';

  try {
    let devices = await navigator.mediaDevices.enumerateDevices();
    let audioInputs = devices.filter(d => d.kind === 'audioinput');

    // If device labels are empty, probe with a temporary getUserMedia stream
    if (audioInputs.length > 0 && !audioInputs[0].label) {
      try {
        const tempStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        devices = await navigator.mediaDevices.enumerateDevices();
        audioInputs = devices.filter(d => d.kind === 'audioinput');
        tempStream.getTracks().forEach(t => t.stop());
      } catch (permErr) {
        console.warn('Mic permission probe error:', permErr);
      }
    }

    selectMicDevice.innerHTML = '';

    if (audioInputs.length === 0) {
      const opt = document.createElement('option');
      opt.value = '';
      opt.textContent = '❌ Tidak ada mikrofon terdeteksi';
      selectMicDevice.appendChild(opt);
      return;
    }

    let preferredDeviceId = '';

    audioInputs.forEach((dev, idx) => {
      const opt = document.createElement('option');
      opt.value = dev.deviceId;
      let label = dev.label || `Mikrofon ${idx + 1}`;
      
      const lower = label.toLowerCase();
      const isVirtual = lower.includes('ideashare') || lower.includes('blackhole') || lower.includes('soundflower') || lower.includes('virtual');
      
      if (isVirtual) {
        label = `⚠️ ${label} (Virtual - Mungkin Hening)`;
      } else if (lower.includes('macbook') || lower.includes('built-in') || lower.includes('internal')) {
        label = `🎙️ ${label} (Bawaan Mac - Direkomendasikan)`;
        if (!preferredDeviceId) preferredDeviceId = dev.deviceId;
      } else if (lower.includes('ys') || lower.includes('yohanes') || lower.includes('usb')) {
        label = `🎙️ ${label} (Mikrofon Eksternal/YS)`;
        if (!preferredDeviceId) preferredDeviceId = dev.deviceId;
      } else {
        label = `🎙️ ${label}`;
        if (!preferredDeviceId && !isVirtual) preferredDeviceId = dev.deviceId;
      }

      opt.textContent = label;
      selectMicDevice.appendChild(opt);
    });

    if (state.selectedDeviceId && audioInputs.some(d => d.deviceId === state.selectedDeviceId)) {
      selectMicDevice.value = state.selectedDeviceId;
    } else if (preferredDeviceId) {
      selectMicDevice.value = preferredDeviceId;
      state.selectedDeviceId = preferredDeviceId;
    } else if (audioInputs.length > 0) {
      selectMicDevice.value = audioInputs[0].deviceId;
      state.selectedDeviceId = audioInputs[0].deviceId;
    }

    // Start live pre-recording monitor on the chosen mic
    startPreMicMonitoring(selectMicDevice.value);

  } catch (err) {
    console.error('enumerateDevices error:', err);
    selectMicDevice.innerHTML = '<option value="">Mikrofon Default (Sistem)</option>';
  }
}

/**
 * Live Pre-Recording Mic Level Monitor & Activity Indicator
 */
async function startPreMicMonitoring(deviceId) {
  stopPreMicMonitoring();

  try {
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (!state.recordAudioContext || state.recordAudioContext.state === 'closed') {
      state.recordAudioContext = new AudioCtx();
    }
    if (state.recordAudioContext.state === 'suspended') {
      await state.recordAudioContext.resume();
    }

    const constraints = {
      audio: {
        echoCancellation: true,
        noiseSuppression: true,
        autoGainControl: true
      }
    };
    if (deviceId) {
      constraints.audio.deviceId = { exact: deviceId };
    }

    let stream;
    try {
      stream = await navigator.mediaDevices.getUserMedia(constraints);
    } catch (e) {
      stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    }

    state.preMicStream = stream;
    const micSource = state.recordAudioContext.createMediaStreamSource(stream);
    const analyser = state.recordAudioContext.createAnalyser();
    analyser.fftSize = 256;
    analyser.smoothingTimeConstant = 0.4;
    micSource.connect(analyser);

    state.preMicSource = micSource;
    state.preMicAnalyser = analyser;

    const dataArray = new Uint8Array(analyser.frequencyBinCount);
    let silentFrameCount = 0;

    const checkVolume = () => {
      if (!state.preMicStream) return;
      state.preMicAnimFrameId = requestAnimationFrame(checkVolume);

      analyser.getByteFrequencyData(dataArray);
      let sum = 0;
      for (let i = 0; i < dataArray.length; i++) {
        sum += dataArray[i];
      }
      const avg = sum / dataArray.length;
      const pct = Math.min(100, Math.round((avg / 90) * 100));

      if (micPreLiveMeter) micPreLiveMeter.style.width = `${pct}%`;
      if (micLiveLevelPct) micLiveLevelPct.textContent = `${pct}%`;

      if (pct > 6) {
        silentFrameCount = 0;
        if (micLiveActivityDot) micLiveActivityDot.className = 'w-2 h-2 rounded-full bg-emerald-400 shadow-sm shadow-emerald-400 animate-pulse';
        if (micLiveActivityText) micLiveActivityText.textContent = 'Suara Terdeteksi! (Mikrofon Aktif)';
        if (micDeviceAdvice) {
          micDeviceAdvice.className = 'text-[10px] text-emerald-400 font-medium leading-tight';
          micDeviceAdvice.textContent = '✅ Bagus! Suara Anda terdeteksi dengan jelas. Silakan klik "Mulai Merekam Suara".';
        }
      } else {
        silentFrameCount++;
        if (silentFrameCount > 60) {
          if (micLiveActivityDot) micLiveActivityDot.className = 'w-2 h-2 rounded-full bg-amber-500';
          if (micLiveActivityText) micLiveActivityText.textContent = 'Menunggu Suara... (Hening)';
          if (micDeviceAdvice) {
            micDeviceAdvice.className = 'text-[10px] text-amber-400 leading-tight';
            micDeviceAdvice.innerHTML = '💡 Silakan berbicara. Jika meteran 0%, ganti pilihan mikrofon ke <b>MacBook Pro Microphone</b> atau <b>YS Microphone</b>.';
          }
        }
      }
    };

    checkVolume();

  } catch (err) {
    console.warn('Pre-mic monitor error:', err);
    if (micLiveActivityText) micLiveActivityText.textContent = 'Status Mikrofon: Siap';
  }
}

/**
 * Stop Live Pre-Recording Monitor
 */
function stopPreMicMonitoring() {
  if (state.preMicAnimFrameId) {
    cancelAnimationFrame(state.preMicAnimFrameId);
    state.preMicAnimFrameId = null;
  }
  if (state.preMicSource) {
    try { state.preMicSource.disconnect(); } catch (e) {}
    state.preMicSource = null;
  }
  if (state.preMicStream) {
    state.preMicStream.getTracks().forEach(t => t.stop());
    state.preMicStream = null;
  }
  if (micPreLiveMeter) micPreLiveMeter.style.width = '0%';
  if (micLiveLevelPct) micLiveLevelPct.textContent = '0%';
}

/**
 * Synthesize Pleasant 2-Tone Speaker Test Chime (Audition Audio Hardware)
 */
function playTestSpeakerChime() {
  try {
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    const actx = new AudioCtx();
    const now = actx.currentTime;

    // Harmonious Chime: E5 (659Hz) -> A5 (880Hz)
    const tones = [
      { freq: 659.25, start: 0, dur: 0.28 },
      { freq: 880.0, start: 0.22, dur: 0.45 }
    ];

    tones.forEach(t => {
      const osc = actx.createOscillator();
      const gain = actx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(t.freq, now + t.start);

      gain.gain.setValueAtTime(0, now + t.start);
      gain.gain.linearRampToValueAtTime(0.3, now + t.start + 0.03);
      gain.gain.exponentialRampToValueAtTime(0.001, now + t.start + t.dur);

      osc.connect(gain);
      gain.connect(actx.destination);

      osc.start(now + t.start);
      osc.stop(now + t.start + t.dur);
    });

    setTimeout(() => {
      try { actx.close(); } catch (e) {}
    }, 1000);

    showToast('🔊 Nada uji speaker diputar. Jika terdengar, speaker Anda berfungsi normal!', 'info');
  } catch (err) {
    console.error('Test chime error:', err);
    showToast('Gagal memutar nada uji speaker: ' + err.message, 'error');
  }
}

/**
 * Open Voice Recording Modal
 */
function openRecordModal(mode = 'trainer') {
  ensureMicSelectorInDOM();
  state.modalCloningType = mode;
  if (!voiceRecordModal) return;

  if (mode === 'trainer') {
    if (modeBtnTrainer) modeBtnTrainer.className = 'py-2 px-3 rounded-xl font-bold bg-amber-500 text-slate-950 text-center transition-all shadow-sm';
    if (modeBtnCustom) modeBtnCustom.className = 'py-2 px-3 rounded-xl font-bold bg-slate-800 text-slate-300 text-center hover:bg-slate-700 transition-all';
    if (labelSpeakerName) labelSpeakerName.textContent = 'Nama AT / Trainer GASING:';
    if (inputSpeakerName) inputSpeakerName.placeholder = 'Contoh: Kak David, Bu Maria...';
    if (modalTitle) modalTitle.textContent = 'Kloning Suara AT (Trainer) GASING';
  } else {
    if (modeBtnTrainer) modeBtnTrainer.className = 'py-2 px-3 rounded-xl font-bold bg-slate-800 text-slate-300 text-center hover:bg-slate-700 transition-all';
    if (modeBtnCustom) modeBtnCustom.className = 'py-2 px-3 rounded-xl font-bold bg-amber-500 text-slate-950 text-center transition-all shadow-sm';
    if (labelSpeakerName) labelSpeakerName.textContent = 'Nama Suara Pribadi Anda:';
    if (inputSpeakerName) inputSpeakerName.placeholder = 'Contoh: Suara Saya (Prof. Muda)...';
    if (modalTitle) modalTitle.textContent = 'Perekam & Kloning Suara Mandiri';
  }

  resetRecordingState();
  voiceRecordModal.classList.remove('hidden');

  // Populate mic devices and initiate live VU sound check
  populateMicDevices();
}

/**
 * Close Voice Recording Modal
 */
function closeRecordModal() {
  if (state.isRecording) {
    stopVoiceRecording();
  }
  stopRecordedSamplePlayback();
  stopPreMicMonitoring();
  if (voiceRecordModal) voiceRecordModal.classList.add('hidden');
}

/**
 * Start In-Browser Voice Recording
 */
async function startVoiceRecording() {
  stopRecordedSamplePlayback();
  stopPreMicMonitoring();

  // Initialize and resume AudioContext immediately on user gesture
  try {
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (!state.recordAudioContext || state.recordAudioContext.state === 'closed') {
      state.recordAudioContext = new AudioCtx();
    }
    if (state.recordAudioContext.state === 'suspended') {
      await state.recordAudioContext.resume();
    }
  } catch (ctxErr) {
    console.warn('AudioContext init error:', ctxErr);
  }

  try {
    const chosenDeviceId = (selectMicDevice && selectMicDevice.value) ? selectMicDevice.value : state.selectedDeviceId;
    const constraints = {
      audio: {
        echoCancellation: true,
        noiseSuppression: true,
        autoGainControl: true
      }
    };
    if (chosenDeviceId) {
      constraints.audio.deviceId = { exact: chosenDeviceId };
    }

    let stream;
    try {
      stream = await navigator.mediaDevices.getUserMedia(constraints);
    } catch (gErr) {
      console.warn('Falling back to default audio constraints:', gErr);
      stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    }

    state.recordStream = stream;
    state.recordedAudioChunks = [];
    state.recordedPcmData = null;
    state.recordedAudioBuffer = null;

    // Connect mic to AnalyserNode for dancing bars visualizer
    if (state.recordAudioContext) {
      try {
        const micSource = state.recordAudioContext.createMediaStreamSource(stream);
        state.recordAnalyser = state.recordAudioContext.createAnalyser();
        state.recordAnalyser.fftSize = 256;
        state.recordAnalyser.smoothingTimeConstant = 0.5;
        micSource.connect(state.recordAnalyser);
        state.recordMicSource = micSource;
      } catch (acErr) {
        console.warn('Analyser connection error:', acErr);
      }
    }

    // Determine optimal supported audio MIME type for MediaRecorder
    const mimeTypes = [
      'audio/webm;codecs=opus',
      'audio/webm',
      'audio/ogg;codecs=opus',
      'audio/mp4',
      'audio/aac',
      ''
    ];
    let selectedMime = '';
    for (const mime of mimeTypes) {
      if (!mime || MediaRecorder.isTypeSupported(mime)) {
        selectedMime = mime;
        break;
      }
    }

    state.mediaRecorder = selectedMime 
      ? new MediaRecorder(stream, { mimeType: selectedMime }) 
      : new MediaRecorder(stream);

    state.mediaRecorder.ondataavailable = (e) => {
      if (e.data && e.data.size > 0) {
        state.recordedAudioChunks.push(e.data);
      }
    };

    state.mediaRecorder.start(100); // collect chunk every 100ms
    state.isRecording = true;

    // UI Updates for RECORDING state
    if (btnToggleRecord) {
      btnToggleRecord.classList.remove('hidden');
      btnToggleRecord.classList.add('recording-active-btn');
      btnToggleRecord.className = 'py-2.5 px-5 rounded-xl text-white text-xs font-bold flex items-center space-x-2 shadow-lg cursor-pointer recording-active-btn';
      if (recordBtnDot) recordBtnDot.className = 'w-3 h-3 rounded-sm bg-white';
      if (btnToggleRecordText) btnToggleRecordText.textContent = '⏹ Selesai & Simpan Rekaman';
    }
    if (recordLed) recordLed.className = 'w-2.5 h-2.5 rounded-full bg-rose-500 animate-pulse shadow-sm shadow-rose-500';
    if (recordStatusLabel) recordStatusLabel.textContent = '🔴 Sedang Merekam Suara... Bacalah naskah di atas';

    if (btnPlayRecordedSample) btnPlayRecordedSample.classList.add('hidden');
    if (btnResetRecord) btnResetRecord.classList.add('hidden');
    if (btnSaveClonedVoice) btnSaveClonedVoice.disabled = true;
    updateModalFooterStatus('Sedang merekam suara...', 'recording');

    // Start Realtime Visualizer & Level Meter
    drawLiveRecordWaveform();

    // Timer
    state.recordSeconds = 0;
    clearInterval(state.recordTimerInterval);
    state.recordTimerInterval = setInterval(() => {
      state.recordSeconds++;
      const mins = String(Math.floor(state.recordSeconds / 60)).padStart(2, '0');
      const secs = String(state.recordSeconds % 60).padStart(2, '0');
      if (recordTimer) recordTimer.textContent = `${mins}:${secs}`;
      if (state.recordSeconds >= 30) {
        stopVoiceRecording();
      }
    }, 1000);

  } catch (err) {
    console.error('Microphone access error:', err);
    showToast('Akses mikrofon gagal atau ditolak browser: ' + err.message, 'error');
    resetRecordingState();
  }
}

/**
 * Stop In-Browser Voice Recording
 */
async function stopVoiceRecording() {
  if (!state.isRecording) return;
  state.isRecording = false;

  clearInterval(state.recordTimerInterval);
  cancelAnimationFrame(state.recordAnimFrameId);

  if (micLevelMeter) micLevelMeter.style.width = '0%';
  if (recordStatusLabel) recordStatusLabel.textContent = 'Memproses dan mengoptimalkan rekaman suara...';

  // Wait for MediaRecorder to stop completely and flush all data
  await new Promise((resolve) => {
    if (!state.mediaRecorder || state.mediaRecorder.state === 'inactive') {
      resolve();
      return;
    }
    state.mediaRecorder.onstop = resolve;
    try {
      state.mediaRecorder.stop();
    } catch (e) {
      resolve();
    }
  });

  // Stop mic stream tracks to release microphone hardware
  if (state.recordStream) {
    state.recordStream.getTracks().forEach(t => t.stop());
    state.recordStream = null;
  }
  if (state.recordMicSource) {
    try { state.recordMicSource.disconnect(); } catch (e) {}
    state.recordMicSource = null;
  }

  const rawMime = (state.mediaRecorder && state.mediaRecorder.mimeType) || 'audio/webm';
  const rawBlob = new Blob(state.recordedAudioChunks, { type: rawMime });

  if (rawBlob.size === 0) {
    showToast('Tidak ada audio tertangkap. Silakan coba merekam kembali.', 'warning');
    resetRecordingState();
    return;
  }

  // Decode audio data into AudioBuffer to inspect real samples and ensure crystal clear loudness
  let audioBuffer = null;
  try {
    const arrayBuffer = await rawBlob.arrayBuffer();
    const decodeCtx = new (window.AudioContext || window.webkitAudioContext)();
    audioBuffer = await decodeCtx.decodeAudioData(arrayBuffer);
    await decodeCtx.close();
  } catch (decErr) {
    console.warn('Audio decoding fallback to raw blob:', decErr);
  }

  if (audioBuffer) {
    state.recordedAudioBuffer = audioBuffer;
    let samples = audioBuffer.getChannelData(0);

    // Calculate peak amplitude
    let maxAmp = 0;
    for (let i = 0; i < samples.length; i++) {
      const abs = Math.abs(samples[i]);
      if (abs > maxAmp) maxAmp = abs;
    }

    // Silence detection: if recording was 100% silent, warn user immediately
    if (maxAmp < 0.005) {
      if (recordStatusLabel) {
        recordStatusLabel.innerHTML = '⚠️ <span class="text-rose-400 font-bold">Rekaman 100% hening!</span> Mikrofon tidak menangkap suara Anda.';
      }
      if (recordLed) recordLed.className = 'w-2.5 h-2.5 rounded-full bg-rose-500 shadow-sm shadow-rose-500';
      showToast('Rekaman hening tanpa suara! Silakan ganti pilihan mikrofon ke "MacBook Pro Microphone" atau "YS Microphone" di dropdown di atas.', 'warning');
      
      if (btnToggleRecord) {
        btnToggleRecord.classList.remove('hidden', 'recording-active-btn');
        btnToggleRecord.className = 'py-2.5 px-5 rounded-xl bg-amber-600 hover:bg-amber-500 text-white text-xs font-bold flex items-center space-x-2 shadow-lg shadow-amber-600/25 transition-all cursor-pointer';
        if (btnToggleRecordText) btnToggleRecordText.textContent = 'Mulai Merekam Suara (Coba Lagi)';
      }
      if (btnResetRecord) btnResetRecord.classList.remove('hidden');
      if (btnSaveClonedVoice) btnSaveClonedVoice.disabled = true;
      updateModalFooterStatus('Rekaman hening!', 'warning');

      // Restart pre-mic monitoring so user can see live meter immediately
      startPreMicMonitoring(selectMicDevice ? selectMicDevice.value : undefined);
      return;
    }

    // Smart gain boost if voice was recorded softly
    if (maxAmp > 0.005 && maxAmp < 0.7) {
      const boost = Math.min(4.0, 0.85 / maxAmp);
      const boosted = new Float32Array(samples.length);
      for (let i = 0; i < samples.length; i++) {
        boosted[i] = Math.max(-1, Math.min(1, samples[i] * boost));
      }
      samples = boosted;
    }

    state.recordedPcmData = samples;
    state.recordedAudioBlob = encodeFloat32ToWavBlob(samples, audioBuffer.sampleRate);
    state.recordSeconds = Math.max(1, Math.round(audioBuffer.duration));
  } else {
    state.recordedAudioBlob = rawBlob;
  }

  if (state.recordedAudioUrl) {
    URL.revokeObjectURL(state.recordedAudioUrl);
  }
  state.recordedAudioUrl = URL.createObjectURL(state.recordedAudioBlob);

  const dur = state.recordSeconds;
  if (recordStatusLabel) recordStatusLabel.textContent = `✅ Rekaman siap (${dur} detik)! Vokal terdeteksi jelas.`;
  if (recordLed) recordLed.className = 'w-2.5 h-2.5 rounded-full bg-emerald-400 shadow-sm shadow-emerald-400';
  updateModalFooterStatus(`Audio siap (${dur} dtk)`, 'success');

  // Render waveform snapshot with true amplitudes
  drawRecordedWaveformSnapshot(0);

  // Hide Record button, show Play and Reset buttons
  if (btnToggleRecord) {
    btnToggleRecord.classList.add('hidden');
    btnToggleRecord.classList.remove('recording-active-btn');
  }

  if (btnPlayRecordedSample) {
    btnPlayRecordedSample.classList.remove('hidden');
    btnPlayRecordedSample.disabled = false;
    btnPlayRecordedSample.className = 'py-2.5 px-5 rounded-xl play-sample-active text-white text-xs font-bold flex items-center space-x-2 transition-all shadow-lg cursor-pointer';
    if (playSampleIcon) playSampleIcon.textContent = '▶';
    if (playSampleText) playSampleText.textContent = `Putar Hasil Rekaman (${dur} dtk)`;
  }

  if (btnResetRecord) {
    btnResetRecord.classList.remove('hidden');
    btnResetRecord.className = 'py-2.5 px-4 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold flex items-center space-x-1.5 border border-slate-700/80 transition-all cursor-pointer';
  }

  // Enable Save Button
  if (btnSaveClonedVoice) btnSaveClonedVoice.disabled = false;
}

/**
 * Draw Animated Realtime Waveform & Live Level Meter
 */
function drawLiveRecordWaveform() {
  if (!recordWaveCanvas || !state.recordAnalyser) return;
  const ctx = recordWaveCanvas.getContext('2d');
  const bufferLength = state.recordAnalyser.frequencyBinCount;
  const dataArray = new Uint8Array(bufferLength);

  const draw = () => {
    if (!state.isRecording) return;
    state.recordAnimFrameId = requestAnimationFrame(draw);
    state.recordAnalyser.getByteFrequencyData(dataArray);

    const w = recordWaveCanvas.width = recordWaveCanvas.offsetWidth || 400;
    const h = recordWaveCanvas.height = recordWaveCanvas.offsetHeight || 64;

    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = '#090d16';
    ctx.fillRect(0, 0, w, h);

    // Center baseline
    ctx.strokeStyle = '#1e293b';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(0, h / 2);
    ctx.lineTo(w, h / 2);
    ctx.stroke();

    let sum = 0;
    const numBars = 48;
    const barWidth = (w / numBars) - 2;

    for (let i = 0; i < numBars; i++) {
      const binIdx = Math.floor((i / numBars) * (bufferLength * 0.7));
      const val = dataArray[binIdx] || 0;
      sum += val;
      const barHeight = Math.max(3, (val / 255) * (h - 8));
      const x = i * (barWidth + 2);
      const y = (h - barHeight) / 2;

      const grad = ctx.createLinearGradient(0, y, 0, y + barHeight);
      grad.addColorStop(0, '#f43f5e'); // Rose
      grad.addColorStop(0.5, '#f59e0b'); // Amber
      grad.addColorStop(1, '#10b981'); // Emerald
      ctx.fillStyle = grad;

      ctx.fillRect(x, y, barWidth, barHeight);
    }

    // Dynamic level meter
    const avg = sum / numBars;
    const levelPct = Math.min(100, Math.round((avg / 110) * 100));
    if (micLevelMeter) micLevelMeter.style.width = `${levelPct}%`;
  };

  draw();
}

/**
 * Play / Pause Preview of Recorded Sample with Dual Engine (HTML5 Audio + WebAudio Fallback)
 */
function togglePlayRecordedSample() {
  if (!state.recordedAudioUrl && !state.recordedAudioBuffer) {
    showToast('Belum ada rekaman suara untuk diputar.', 'warning');
    return;
  }

  const dur = state.recordSeconds || 1;

  if (state.isPreviewPlaying) {
    stopRecordedSamplePlayback();
    return;
  }

  // Ensure clean stop of any previous playback
  stopRecordedSamplePlayback();

  // Ensure AudioContext is ready for playback
  try {
    if (state.recordAudioContext && state.recordAudioContext.state === 'suspended') {
      state.recordAudioContext.resume();
    }
  } catch (e) {}

  state.isPreviewPlaying = true;
  if (playSampleIcon) playSampleIcon.textContent = '⏸';
  if (playSampleText) playSampleText.textContent = 'Jeda Pemutaran';
  if (btnPlayRecordedSample) btnPlayRecordedSample.classList.add('play-sample-playing');

  // Primary: HTML5 Audio Element
  const audio = new Audio();
  audio.src = state.recordedAudioUrl;
  audio.volume = 1.0;
  state.previewAudio = audio;

  audio.ontimeupdate = () => {
    if (audio && audio.duration && !isNaN(audio.duration) && audio.duration > 0) {
      const pct = (audio.currentTime / audio.duration) * 100;
      drawRecordedWaveformSnapshot(pct);
    }
  };

  audio.onended = () => {
    stopRecordedSamplePlayback();
  };

  audio.onerror = (e) => {
    console.warn('HTML5 Audio preview error, attempting Web Audio buffer playback:', e);
    playViaWebAudioBuffer();
  };

  const playPromise = audio.play();
  if (playPromise !== undefined) {
    playPromise.catch((err) => {
      console.warn('audio.play() prevented, falling back to Web Audio buffer:', err);
      playViaWebAudioBuffer();
    });
  }
}

/**
 * Fallback Web Audio Buffer Playback (zero-failure, direct in-memory PCM output)
 */
function playViaWebAudioBuffer() {
  if (!state.recordedAudioBuffer) {
    stopRecordedSamplePlayback();
    return;
  }
  try {
    const actx = new (window.AudioContext || window.webkitAudioContext)();
    if (actx.state === 'suspended') actx.resume();

    const source = actx.createBufferSource();
    source.buffer = state.recordedAudioBuffer;
    source.connect(actx.destination);

    const startTime = actx.currentTime;
    const duration = state.recordedAudioBuffer.duration;

    const scrub = () => {
      if (!state.isPreviewPlaying) return;
      const elapsed = actx.currentTime - startTime;
      const pct = Math.min(100, (elapsed / duration) * 100);
      drawRecordedWaveformSnapshot(pct);
      if (elapsed < duration) {
        state.previewScrubAnimId = requestAnimationFrame(scrub);
      }
    };
    state.previewScrubAnimId = requestAnimationFrame(scrub);

    source.onended = () => {
      stopRecordedSamplePlayback();
      try { actx.close(); } catch (e) {}
    };

    source.start(0);
    state.previewBufferSource = source;
  } catch (wbErr) {
    console.error('WebAudio buffer playback error:', wbErr);
    stopRecordedSamplePlayback();
    showToast('Gagal memutar rekaman: ' + wbErr.message, 'error');
  }
}

/**
 * Save Cloned Voice (Trainer or Custom) to Backend
 */
async function saveClonedVoice() {
  const name = inputSpeakerName ? inputSpeakerName.value.trim() : '';
  if (!name) {
    showToast('Harap masukkan nama AT / Pemilik Suara!', 'warning');
    if (inputSpeakerName) inputSpeakerName.focus();
    return;
  }

  const hasRecorded = !!state.recordedAudioBlob;
  const hasFile = modalAudioFileInput && modalAudioFileInput.files && modalAudioFileInput.files[0];

  if (!hasRecorded && !hasFile) {
    showToast('Rekam suara mikrofon atau pilih file audio terlebih dahulu!', 'warning');
    return;
  }

  btnSaveClonedVoice.disabled = true;
  btnSaveClonedVoice.textContent = 'Memproses Model Kloning...';

  try {
    const formData = new FormData();

    if (hasFile) {
      formData.append(state.modalCloningType === 'trainer' ? 'audio_file' : 'file', modalAudioFileInput.files[0]);
    } else {
      const file = new File([state.recordedAudioBlob], `recorded_${Date.now()}.wav`, { type: 'audio/wav' });
      formData.append(state.modalCloningType === 'trainer' ? 'audio_file' : 'file', file);
    }

    formData.append('name', name);
    formData.append('ref_text', inputRefText ? inputRefText.value.trim() : '');
    formData.append('gender', selectGender ? selectGender.value : 'Pria');

    let endpoint = '/api/f5/clone-trainer';
    if (state.modalCloningType === 'trainer') {
      formData.append('role', selectNarratorRole ? selectNarratorRole.value : 'Narator Modul Matematika SO');
      formData.append('region', inputRegion ? inputRegion.value.trim() : 'Indonesia');
      endpoint = '/api/f5/clone-trainer';
    } else {
      formData.append('category', 'custom');
      formData.append('role', selectNarratorRole ? selectNarratorRole.value : 'Narator Kustom');
      formData.append('region', inputRegion ? inputRegion.value.trim() : '');
      formData.append('description', 'Model suara kustom pengguna');
      endpoint = '/api/f5/clone-voice';
    }

    const res = await fetch(endpoint, {
      method: 'POST',
      body: formData
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Gagal menyimpan profil kloning suara');
    }

    const data = await res.json();
    showToast(`Model suara ${name} berhasil dibuat dan siap digunakan!`, 'success');

    closeRecordModal();
    await loadF5Voices();

    if (data.profile && data.profile.id) {
      selectF5Voice(data.profile.id);
    }

  } catch (err) {
    console.error('saveClonedVoice error:', err);
    showToast('Gagal menyimpan kloning: ' + err.message, 'error');
  } finally {
    btnSaveClonedVoice.disabled = false;
    btnSaveClonedVoice.textContent = 'Simpan & Buat Model Suara';
  }
}

/**
 * Auto Clone Marcia Quick Action (Female Trainer from 6-minute master)
 */
async function triggerAutoCloneMarcia() {
  if (!btnAutoCloneMarcia) return;
  const originalHtml = btnAutoCloneMarcia.innerHTML;
  btnAutoCloneMarcia.disabled = true;

  try {
    showToast('Mengekstrak sampel suara Guru Marcia dari rekaman master 6 menit...', 'info');
    const res = await fetch('/api/f5/auto-clone-marcia', { method: 'POST' });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Gagal auto-clone Marcia');
    }
    showToast('Suara Guru Marcia (Trainer Marcia Asli) berhasil diekstrak!', 'success');
    await loadF5Voices();
    selectF5Voice('so_marcia');
  } catch (err) {
    showToast('Error ekstraksi Marcia: ' + err.message, 'error');
  } finally {
    btnAutoCloneMarcia.disabled = false;
    btnAutoCloneMarcia.innerHTML = originalHtml;
  }
}

/**
 * Auto Clone John Quick Action (Male Trainer from Tanya Marcia video)
 */
async function triggerAutoCloneJohn() {
  if (!btnAutoCloneJohn) return;
  const originalHtml = btnAutoCloneJohn.innerHTML;
  btnAutoCloneJohn.disabled = true;

  try {
    showToast('Mengekstrak suara Tutor John dari video Tanya Marcia...', 'info');
    const res = await fetch('/api/f5/auto-clone-john', { method: 'POST' });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Gagal auto-clone John');
    }
    showToast('Suara Tutor John (Video Tanya Marcia - Pria) berhasil diekstrak!', 'success');
    await loadF5Voices();
    selectF5Voice('at_john');
  } catch (err) {
    showToast('Error ekstraksi John: ' + err.message, 'error');
  } finally {
    btnAutoCloneJohn.disabled = false;
    btnAutoCloneJohn.innerHTML = originalHtml;
  }
}

/**
 * Auto Clone Prof Yohanes Surya Quick Action
 */
async function triggerAutoCloneProf() {
  if (!btnAutoCloneProf) return;
  const originalHtml = btnAutoCloneProf.innerHTML;
  btnAutoCloneProf.disabled = true;

  try {
    showToast('Mengkloning suara autentik Prof. Yohanes Surya...', 'info');
    const res = await fetch('/api/f5/auto-clone-prof', { method: 'POST' });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Gagal auto-clone Prof');
    }
    showToast('Suara Yosu (Prof. Yohanes Surya) siap digunakan!', 'success');
    await loadF5Voices();
    const targetVoice = state.f5Voices.find(v => v.id === 'so_yosu' || v.id === 'prof_yosu_asli');
    if (targetVoice) selectF5Voice(targetVoice.id);
  } catch (err) {
    showToast('Error kloning Prof: ' + err.message, 'error');
  } finally {
    btnAutoCloneProf.disabled = false;
    btnAutoCloneProf.innerHTML = originalHtml;
  }
}

/**
 * Setup Event Listeners
 */
function setupEventListeners() {
  // Tab Switching (TTS, Soundboard, F5-TTS Indo, Proyek Video)
  if (tabBtnTTS) tabBtnTTS.addEventListener('click', () => switchTab('tts'));
  if (tabBtnSoundboard) tabBtnSoundboard.addEventListener('click', () => switchTab('soundboard'));
  if (tabBtnF5) tabBtnF5.addEventListener('click', () => switchTab('f5'));
  if (tabBtnVideoProject) tabBtnVideoProject.addEventListener('click', () => switchTab('videoproject'));

  // Proyek Video Controls
  if (projectSelectDropdown) {
    projectSelectDropdown.addEventListener('change', (e) => {
      loadVideoProjectData(e.target.value);
    });
  }

  if (btnVoiceModeF5) btnVoiceModeF5.addEventListener('click', () => setVideoProjectVoiceMode('f5'));
  if (btnVoiceModeEdge) btnVoiceModeEdge.addEventListener('click', () => setVideoProjectVoiceMode('edge'));

  if (btnDualPlay) {
    btnDualPlay.addEventListener('click', () => {
      if (videoOriginal && videoDubbed) {
        const curTime = Math.min(videoOriginal.currentTime, videoDubbed.currentTime);
        videoOriginal.currentTime = curTime;
        videoDubbed.currentTime = curTime;
        videoOriginal.play();
        videoDubbed.play();
      }
    });
  }

  if (btnStopBoth) {
    btnStopBoth.addEventListener('click', () => {
      if (videoOriginal) {
        videoOriginal.pause();
        videoOriginal.currentTime = 0;
      }
      if (videoDubbed) {
        videoDubbed.pause();
        videoDubbed.currentTime = 0;
      }
    });
  }

  const btnReloadF5Voices = document.getElementById('btnReloadF5Voices');
  if (btnReloadF5Voices) {
    btnReloadF5Voices.addEventListener('click', async () => {
      showToast('🔄 Memperbarui daftar suara...', 'info');
      await loadF5Voices();
    });
  }

  // Global & Soundboard Search
  const handleSearch = (e) => {
    state.searchQuery = e.target.value;
    // Switch to soundboard tab if searching globally
    if (e.target === globalSearchInput && state.searchQuery.trim()) {
      tabBtnSoundboard.click();
    }
    renderSoundboard();
  };
  globalSearchInput.addEventListener('input', handleSearch);
  soundboardSearchInput.addEventListener('input', handleSearch);

  // Category Filter Pills
  document.querySelectorAll('.cat-filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.cat-filter-btn').forEach(b => {
        b.className = 'cat-filter-btn px-3 py-1.5 rounded-xl text-xs font-semibold bg-slate-800 text-slate-300 hover:bg-slate-700 transition-all';
      });
      btn.className = 'cat-filter-btn px-3 py-1.5 rounded-xl text-xs font-semibold bg-indigo-600 text-white shadow-sm transition-all';
      state.currentCategoryFilter = btn.getAttribute('data-cat');
      renderSoundboard();
    });
  });

  // Character Cards Selection
  document.querySelectorAll('.character-card').forEach(card => {
    card.addEventListener('click', () => {
      document.querySelectorAll('.character-card').forEach(c => c.classList.remove('active'));
      card.classList.add('active');

      const charId = card.getAttribute('data-char');
      state.selectedCharacter = charId;
      state.selectedVoice = card.getAttribute('data-voice');
      state.selectedPitchStr = card.getAttribute('data-pitch');
      state.selectedRateStr = card.getAttribute('data-rate');

      const preset = characterPresets[charId];
      if (preset) {
        selectedCharBadge.textContent = preset.name;
        currentAudioTitle.textContent = preset.name;
        // Adjust tuner sliders to match character signature
        setPitchSemitones(preset.semitones);
        setSpeedFactor(preset.speed);
      }
    });
  });

  // Sample Dialogue Preset Buttons
  const btnBabilon = document.getElementById('btnPresetBabilon');
  if (btnBabilon) {
    btnBabilon.addEventListener('click', () => {
      narrationInput.value = presetTexts.babilon;
      updateTextStats();
      const card = document.querySelector('.character-card[data-char="prof_gasing_mentor"]');
      if (card) card.click();
      loadAssetIntoStudio('/assets/audio/prof_gasing/01_prof_gasing_misi_babilon.wav', 'Prof. Gasing (Misi Babilonia)');
      state.lastGeneratedText = presetTexts.babilon;
      state.lastGeneratedChar = 'prof_gasing_mentor';
    });
  }

  const btnAnak = document.getElementById('btnPresetAnak');
  if (btnAnak) {
    btnAnak.addEventListener('click', () => {
      narrationInput.value = presetTexts.anakCeria;
      updateTextStats();
      const card = document.querySelector('.character-card[data-char="vo_anak_ceria"]');
      if (card) card.click();
      loadAssetIntoStudio('/assets/audio/contoh_voiceover/01_suara_anak_ceria.mp3', '👶 Suara Anak Ceria (Kids Voice)');
      state.lastGeneratedText = presetTexts.anakCeria;
      state.lastGeneratedChar = 'vo_anak_ceria';
    });
  }

  const btnKorporat = document.getElementById('btnPresetKorporat');
  if (btnKorporat) {
    btnKorporat.addEventListener('click', () => {
      narrationInput.value = presetTexts.korporat;
      updateTextStats();
      const card = document.querySelector('.character-card[data-char="vo_korporat_formal"]');
      if (card) card.click();
      loadAssetIntoStudio('/assets/audio/contoh_voiceover/02_suara_korporat_profesional.mp3', '🏢 Suara Korporat Profesional');
      state.lastGeneratedText = presetTexts.korporat;
      state.lastGeneratedChar = 'vo_korporat_formal';
    });
  }

  const btnVlog = document.getElementById('btnPresetVlog');
  if (btnVlog) {
    btnVlog.addEventListener('click', () => {
      narrationInput.value = presetTexts.youtubeVlog;
      updateTextStats();
      const card = document.querySelector('.character-card[data-char="vo_youtube_vlog"]');
      if (card) card.click();
      loadAssetIntoStudio('/assets/audio/contoh_voiceover/03_suara_youtube_vlog.mp3', '📹 Suara YouTube & Daily Vlog');
      state.lastGeneratedText = presetTexts.youtubeVlog;
      state.lastGeneratedChar = 'vo_youtube_vlog';
    });
  }

  const btnAudiobook = document.getElementById('btnPresetAudiobook');
  if (btnAudiobook) {
    btnAudiobook.addEventListener('click', () => {
      narrationInput.value = presetTexts.audiobook;
      updateTextStats();
      const card = document.querySelector('.character-card[data-char="vo_audiobook_kisah"]');
      if (card) card.click();
      loadAssetIntoStudio('/assets/audio/contoh_voiceover/04_suara_audiobook_kisah.mp3', '📚 Suara Audiobook & Cerita');
      state.lastGeneratedText = presetTexts.audiobook;
      state.lastGeneratedChar = 'vo_audiobook_kisah';
    });
  }

  const btnIklan = document.getElementById('btnPresetIklan');
  if (btnIklan) {
    btnIklan.addEventListener('click', () => {
      narrationInput.value = presetTexts.iklanKomersial;
      updateTextStats();
      const card = document.querySelector('.character-card[data-char="vo_iklan_komersial"]');
      if (card) card.click();
      loadAssetIntoStudio('/assets/audio/contoh_voiceover/05_suara_iklan_komersial.mp3', '🎧 Suara Iklan & Komersial');
      state.lastGeneratedText = presetTexts.iklanKomersial;
      state.lastGeneratedChar = 'vo_iklan_komersial';
    });
  }

  const btnMotivator = document.getElementById('btnPresetMotivator');
  if (btnMotivator) {
    btnMotivator.addEventListener('click', () => {
      narrationInput.value = presetTexts.motivatorPria;
      updateTextStats();
      const card = document.querySelector('.character-card[data-char="vo_motivator_pria"]');
      if (card) card.click();
      loadAssetIntoStudio('/assets/audio/contoh_voiceover/06_suara_motivator_pria.mp3', '⚡ Suara Motivator Pria Energik');
      state.lastGeneratedText = presetTexts.motivatorPria;
      state.lastGeneratedChar = 'vo_motivator_pria';
    });
  }

  const btnLirikKanan = document.getElementById('btnPresetLirikKanan');
  if (btnLirikKanan) {
    btnLirikKanan.addEventListener('click', () => {
      narrationInput.value = presetTexts.lirikKanan;
      updateTextStats();
      const card = document.querySelector('.character-card[data-char="master_tutor"]');
      if (card) card.click();
      loadAssetIntoStudio('/assets/audio/karakter_lain/master_tutor_lirik_kanan.wav', 'Master Tutor (Trik Lirik Kanan)');
      state.lastGeneratedText = presetTexts.lirikKanan;
      state.lastGeneratedChar = 'master_tutor';
    });
  }

  const btnPujianCeria = document.getElementById('btnPresetPujianCeria');
  if (btnPujianCeria) {
    btnPujianCeria.addEventListener('click', () => {
      narrationInput.value = presetTexts.pujianCeria;
      updateTextStats();
      const card = document.querySelector('.character-card[data-char="prof_gasing_anime"]');
      if (card) card.click();
      loadAssetIntoStudio('/assets/audio/pujian_gasing/22_Kasih_We_o_We_WOW.mp3', 'Kasih W O W (Asset Asli Bowo)');
      state.lastGeneratedText = presetTexts.pujianCeria;
      state.lastGeneratedChar = 'prof_gasing_anime';
    });
  }

  document.getElementById('btnClearText').addEventListener('click', () => {
    narrationInput.value = '';
    updateTextStats();
    stopPlayback();
  });

  document.getElementById('btnPasteText').addEventListener('click', async () => {
    try {
      if (navigator.clipboard && navigator.clipboard.readText) {
        const text = await navigator.clipboard.readText();
        if (text) {
          narrationInput.value += (narrationInput.value ? '\n' : '') + text;
          updateTextStats();
          showToast('Teks berhasil ditempel dari clipboard!', 'success');
          return;
        }
      }
      narrationInput.focus();
      showToast('Gunakan shortcut keyboard Ctrl+V atau Cmd+V.', 'info');
    } catch (e) {
      narrationInput.focus();
      showToast('Gunakan shortcut keyboard Ctrl+V atau Cmd+V.', 'info');
    }
  });

  narrationInput.addEventListener('input', updateTextStats);

  // Smart Match Button
  btnLoadSmartMatch.addEventListener('click', () => {
    if (currentMatchedAsset) {
      loadAssetIntoStudio(currentMatchedAsset.rel_path, currentMatchedAsset.title);
      startPlayback();
    }
  });

  // Vibe Selector Buttons
  document.querySelectorAll('.vibe-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.vibe-btn').forEach(b => b.classList.remove('active', 'border-indigo-500', 'bg-indigo-950/40'));
      btn.classList.add('active', 'border-indigo-500', 'bg-indigo-950/40');
      const v = btn.getAttribute('data-vibe');
      state.selectedVibe = v;
      vibeBadge.textContent = v.charAt(0).toUpperCase() + v.slice(1);
    });
  });

  // Generate TTS Action
  btnGenerateTTS.addEventListener('click', generateTTS);

  // Main Player Actions
  btnMainPlay.addEventListener('click', () => {
    if (state.isPlaying) {
      pausePlayback();
    } else {
      startPlayback();
    }
  });

  btnMainStop.addEventListener('click', stopPlayback);

  btnMainLoop.addEventListener('click', () => {
    state.isLooping = !state.isLooping;
    if (state.isLooping) {
      btnMainLoop.className = 'btn-subtle p-2.5 text-indigo-400 border-indigo-500/50 bg-indigo-950/40';
      showToast('Mode Loop aktif.', 'info');
    } else {
      btnMainLoop.className = 'btn-subtle p-2.5 text-slate-400 hover:text-indigo-300';
    }
  });

  seekSlider.addEventListener('input', (e) => {
    if (state.audioElement && state.audioElement.duration) {
      const targetTime = (parseFloat(e.target.value) / 100) * state.audioElement.duration;
      state.audioElement.currentTime = targetTime;
    }
  });

  // ==========================================
  // DSP TUNER SLIDERS (Pitch, Speed, Bass, Treble, Volume)
  // ==========================================
  pitchSlider.addEventListener('input', (e) => {
    setPitchSemitones(parseFloat(e.target.value));
  });

  document.querySelectorAll('.pitch-preset-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const p = parseFloat(btn.getAttribute('data-pitch'));
      pitchSlider.value = p;
      setPitchSemitones(p);
    });
  });

  speedSlider.addEventListener('input', (e) => {
    setSpeedFactor(parseFloat(e.target.value));
  });

  document.querySelectorAll('.speed-preset-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const s = parseFloat(btn.getAttribute('data-speed'));
      speedSlider.value = s;
      setSpeedFactor(s);
    });
  });

  bassSlider.addEventListener('input', (e) => {
    state.bassGain = parseFloat(e.target.value);
    bassBadge.textContent = `${state.bassGain > 0 ? '+' : ''}${state.bassGain} dB`;
    applyDSPParameters();
  });

  trebleSlider.addEventListener('input', (e) => {
    state.trebleGain = parseFloat(e.target.value);
    trebleBadge.textContent = `${state.trebleGain > 0 ? '+' : ''}${state.trebleGain} dB`;
    applyDSPParameters();
  });

  volumeSlider.addEventListener('input', (e) => {
    state.volumeGain = parseFloat(e.target.value);
    volumeBadge.textContent = `${Math.round(state.volumeGain * 100)}%`;
    applyDSPParameters();
  });

  // Download Actions (Dual Format: WAV Master & MP3 320k)
  if (btnDownloadWav) btnDownloadWav.addEventListener('click', downloadProcessedWav);
  if (btnDownloadMp3) btnDownloadMp3.addEventListener('click', downloadProcessedMp3);

  // ==========================================
  // F5-TTS INDO STUDIO EVENT LISTENERS
  // ==========================================

  // Category Filter Pills
  document.querySelectorAll('.f5-cat-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.f5-cat-btn').forEach(b => {
        b.className = 'f5-cat-btn px-3 py-1 rounded-xl font-semibold bg-slate-800 text-slate-300 hover:bg-slate-700 transition-all';
      });
      btn.className = 'f5-cat-btn px-3 py-1 rounded-xl font-semibold bg-amber-500 text-slate-950 shadow-sm transition-all';
      state.selectedF5Category = btn.getAttribute('data-f5cat');
      renderF5VoiceGrid();
    });
  });

  // Quick Action Auto-Cloners & Record Launchers
  if (btnAutoCloneMarcia) btnAutoCloneMarcia.addEventListener('click', triggerAutoCloneMarcia);
  if (btnAutoCloneJohn) btnAutoCloneJohn.addEventListener('click', triggerAutoCloneJohn);
  if (btnAutoCloneProf) btnAutoCloneProf.addEventListener('click', triggerAutoCloneProf);
  if (btnOpenVoiceRecorder) btnOpenVoiceRecorder.addEventListener('click', () => openRecordModal('trainer'));
  if (btnOpenAudioUpload) btnOpenAudioUpload.addEventListener('click', () => {
    openRecordModal('trainer');
    setTimeout(() => { if (modalAudioFileInput) modalAudioFileInput.click(); }, 150);
  });

  // Modal Controls
  if (btnCloseRecordModal) btnCloseRecordModal.addEventListener('click', closeRecordModal);
  if (btnCancelRecordModal) btnCancelRecordModal.addEventListener('click', closeRecordModal);
  if (modeBtnTrainer) modeBtnTrainer.addEventListener('click', () => openRecordModal('trainer'));
  if (modeBtnCustom) modeBtnCustom.addEventListener('click', () => openRecordModal('custom'));
  if (btnSwitchCalibScript) btnSwitchCalibScript.addEventListener('click', () => {
    currentCalibScriptIdx = (currentCalibScriptIdx + 1) % trainerCalibScripts.length;
    if (inputRefText) inputRefText.value = trainerCalibScripts[currentCalibScriptIdx];
    showToast('Naskah kalibrasi diganti.', 'info');
  });

  // Microphone Selector & Speaker Test Actions
  if (btnTestSpeakerChime) {
    btnTestSpeakerChime.addEventListener('click', playTestSpeakerChime);
  }
  if (btnRefreshMicDevices) {
    btnRefreshMicDevices.addEventListener('click', async () => {
      await populateMicDevices();
      showToast('Daftar mikrofon diperbarui.', 'info');
    });
  }
  if (selectMicDevice) {
    selectMicDevice.addEventListener('change', (e) => {
      state.selectedDeviceId = e.target.value;
      startPreMicMonitoring(e.target.value);
    });
  }

  // Recording Actions
  if (btnToggleRecord) {
    btnToggleRecord.addEventListener('click', async () => {
      if (state.isRecording) {
        await stopVoiceRecording();
      } else {
        await startVoiceRecording();
      }
    });
  }

  if (btnPlayRecordedSample) {
    btnPlayRecordedSample.addEventListener('click', togglePlayRecordedSample);
  }

  if (btnResetRecord) {
    btnResetRecord.addEventListener('click', () => {
      resetRecordingState();
      showToast('Rekaman direset. Anda dapat mulai merekam kembali.', 'info');
    });
  }

  if (btnTriggerFileSelect) {
    btnTriggerFileSelect.addEventListener('click', () => {
      if (modalAudioFileInput) modalAudioFileInput.click();
    });
  }

  if (modalAudioFileInput) {
    modalAudioFileInput.addEventListener('change', async (e) => {
      const file = e.target.files && e.target.files[0];
      if (file) {
        if (selectedFileNameDisplay) {
          selectedFileNameDisplay.textContent = `📁 File dipilih: ${file.name} (${(file.size / 1024 / 1024).toFixed(1)} MB)`;
        }
        
        state.recordedAudioBlob = file;
        if (state.recordedAudioUrl) {
          URL.revokeObjectURL(state.recordedAudioUrl);
        }
        state.recordedAudioUrl = URL.createObjectURL(file);

        // Try decoding audio for waveform preview
        try {
          const slice = file.slice(0, 8 * 1024 * 1024);
          const buf = await slice.arrayBuffer();
          const actx = new (window.AudioContext || window.webkitAudioContext)();
          const decoded = await actx.decodeAudioData(buf);
          actx.close();
          state.recordedPcmData = decoded.getChannelData(0);
          state.recordSeconds = Math.round(decoded.duration);
          const mins = String(Math.floor(state.recordSeconds / 60)).padStart(2, '0');
          const secs = String(state.recordSeconds % 60).padStart(2, '0');
          if (recordTimer) recordTimer.textContent = `${mins}:${secs}`;
          drawRecordedWaveformSnapshot(0);
        } catch (decErr) {
          console.warn('File decode preview skipped:', decErr);
        }

        if (recordStatusLabel) recordStatusLabel.textContent = `✅ File audio siap (${file.name})`;
        if (recordLed) recordLed.className = 'w-2.5 h-2.5 rounded-full bg-emerald-400 shadow-sm shadow-emerald-400';

        if (btnToggleRecord) btnToggleRecord.classList.add('hidden');
        if (btnPlayRecordedSample) {
          btnPlayRecordedSample.classList.remove('hidden');
          btnPlayRecordedSample.disabled = false;
          btnPlayRecordedSample.className = 'py-2.5 px-5 rounded-xl play-sample-active text-white text-xs font-bold flex items-center space-x-2 transition-all shadow-lg cursor-pointer';
          if (playSampleIcon) playSampleIcon.textContent = '▶';
          if (playSampleText) playSampleText.textContent = `Putar File Terpilih (${state.recordSeconds || 'Audio'})`;
        }
        if (btnResetRecord) btnResetRecord.classList.remove('hidden');
        if (btnSaveClonedVoice) btnSaveClonedVoice.disabled = false;
        updateModalFooterStatus(`File siap (${(file.size / 1024 / 1024).toFixed(1)} MB)`, 'success');
      }
    });
  }

  if (btnSaveClonedVoice) btnSaveClonedVoice.addEventListener('click', saveClonedVoice);

  // F5 Narration & Pronunciation Preview Listeners
  if (f5NarrationInput) {
    f5NarrationInput.addEventListener('input', updateF5PronunciationPreview);
  }
  if (f5BilingualSwitch) {
    f5BilingualSwitch.addEventListener('change', updateF5PronunciationPreview);
  }
  if (btnF5ClearText) {
    btnF5ClearText.addEventListener('click', () => {
      if (f5NarrationInput) f5NarrationInput.value = '';
      updateF5PronunciationPreview();
    });
  }

  // Praise Chips
  document.querySelectorAll('.f5-praise-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      const praiseText = chip.getAttribute('data-praise');
      if (f5NarrationInput && praiseText) {
        const current = f5NarrationInput.value.trim();
        f5NarrationInput.value = current ? `${current}\n${praiseText}` : praiseText;
        updateF5PronunciationPreview();
        f5NarrationInput.focus();
        showToast('Ucapan pujian GASING disisipkan ke naskah!', 'success');
      }
    });
  });

  // F5 Speed Slider
  if (f5SpeedSlider) {
    f5SpeedSlider.addEventListener('input', (e) => {
      if (f5SpeedLabel) f5SpeedLabel.textContent = `${parseFloat(e.target.value).toFixed(2)}x`;
    });
  }

  // Generate F5 Button
  if (btnGenerateF5TTS) {
    btnGenerateF5TTS.addEventListener('click', generateF5TTS);
  }

  // Resize canvas handler
  window.addEventListener('resize', initCanvas);
}

function setPitchSemitones(val) {
  state.pitchSemitones = val;
  const sign = val > 0 ? '+' : '';
  pitchBadge.textContent = `${sign}${val.toFixed(1)} st`;

  // Highlight active preset button
  document.querySelectorAll('.pitch-preset-btn').forEach(btn => {
    if (parseFloat(btn.getAttribute('data-pitch')) === val) {
      btn.className = 'pitch-preset-btn btn-subtle py-1 text-center active border-indigo-500 text-indigo-300';
    } else {
      btn.className = 'pitch-preset-btn btn-subtle py-1 text-center';
    }
  });

  applyDSPParameters();
}

function setSpeedFactor(val) {
  state.speedFactor = val;
  speedBadge.textContent = `${val.toFixed(2)}x`;

  document.querySelectorAll('.speed-preset-btn').forEach(btn => {
    if (parseFloat(btn.getAttribute('data-speed')) === val) {
      btn.className = 'speed-preset-btn btn-subtle py-1 text-center active border-indigo-500 text-indigo-300';
    } else {
      btn.className = 'speed-preset-btn btn-subtle py-1 text-center';
    }
  });

  applyDSPParameters();
}

// App Initialization (Immediate on DOM ready)
function initializeVoiceOverApp() {
  if (window.__VOICEOVER_INITIALIZED) return;
  window.__VOICEOVER_INITIALIZED = true;

  initCanvas();
  renderVisualizer();
  ensureMicSelectorInDOM();
  setupEventListeners();

  // Load default preset text
  if (narrationInput) narrationInput.value = presetTexts.babilon;
  updateTextStats();

  // Pre-load default audio so "Putar Suara" produces sound immediately!
  loadAssetIntoStudio('/assets/audio/prof_gasing/01_prof_gasing_misi_babilon.wav', 'Prof. Gasing (Misi Babilonia)');
  state.lastGeneratedText = presetTexts.babilon;
  state.lastGeneratedChar = 'prof_gasing_mentor';

  // Load catalog
  loadCatalog();

  // Initialize F5-TTS Indo Studio
  loadF5Voices();
  checkF5Status();
  updateF5PronunciationPreview();

  // Check URL hash for direct tab navigation (/proyek-video)
  if (window.location.hash === '#/proyek-video' || window.location.pathname.includes('proyek-video')) {
    switchTab('videoproject');
  }
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeVoiceOverApp);
} else {
  initializeVoiceOverApp();
}
window.addEventListener('load', initializeVoiceOverApp);

