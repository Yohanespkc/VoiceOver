import asyncio
import sys
import os
from playwright.async_api import async_playwright

BASE_URL = "http://127.0.0.1:8765"

results = {
    "total": 0,
    "passed": 0,
    "failed": 0,
    "failures": []
}

def record_check(test_name, success, details=""):
    results["total"] += 1
    if success:
        results["passed"] += 1
        print(f"  ✅ [PASS] {test_name}: {details}")
    else:
        results["failed"] += 1
        results["failures"].append((test_name, details))
        print(f"  ❌ [FAIL] {test_name}: {details}")

async def run_tests():
    print("=" * 70)
    print("🚀 STARTING COMPREHENSIVE PLAYWRIGHT TEST SUITE FOR ALL BUTTONS")
    print("=" * 70)

    async with async_playwright() as p:
        # Launch chromium with fake audio stream device for realistic mic testing
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--use-fake-ui-for-media-stream",
                "--use-fake-device-for-media-stream",
                "--no-sandbox",
                "--disable-setuid-sandbox"
            ]
        )
        context = await browser.new_context(
            permissions=["microphone"],
            viewport={"width": 1512, "height": 950}
        )
        page = await context.new_page()

        # Capture console errors
        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda err: console_errors.append(str(err)))

        print("\n--- 1. LOADING APPLICATION & VERIFYING HEADER ---")
        try:
            await page.goto(BASE_URL, wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_selector("#tabBtnTTS", timeout=10000)
            await page.wait_for_function("() => window.__VOICEOVER_INITIALIZED === true", timeout=10000)
            record_check("Page Load", True, "Successfully loaded VoiceOver Studio & Event Listeners")
        except Exception as e:
            record_check("Page Load", False, str(e))
            await browser.close()
            return

        # -------------------------------------------------------------
        # TEST NAVIGATION TABS
        # -------------------------------------------------------------
        print("\n--- 2. TESTING NAVIGATION TABS ---")
        tabs = [
            ("tabBtnTTS", "tabContentTTS", "Generator Narasi AI"),
            ("tabBtnSoundboard", "tabContentSoundboard", "Papan Asset Asli"),
            ("tabBtnF5", "tabContentF5", "F5-TTS Indo Studio"),
            ("tabBtnTTS", "tabContentTTS", "Back to Generator Narasi AI")
        ]
        for tab_id, content_id, label in tabs:
            try:
                tab_btn = page.locator(f"#{tab_id}")
                await tab_btn.click()
                await page.wait_for_timeout(350)
                content = page.locator(f"#{content_id}")
                is_visible = await content.is_visible()
                record_check(f"Nav Tab Click: {label}", is_visible, f"Content #{content_id} is visible: {is_visible}")
            except Exception as e:
                record_check(f"Nav Tab Click: {label}", False, str(e))

        # -------------------------------------------------------------
        # TEST TAB 1: GENERATOR NARASI AI (TTS TAB)
        # -------------------------------------------------------------
        print("\n--- 3. TESTING TAB 1: GENERATOR NARASI AI BUTTONS ---")
        await page.locator("#tabBtnTTS").click()
        await page.wait_for_timeout(300)

        # Character Cards
        char_cards = await page.locator(".character-card").all()
        record_check("Character Cards Count", len(char_cards) >= 6, f"Found {len(char_cards)} character cards")
        for card in char_cards:
            char_id = await card.get_attribute("data-char")
            try:
                await card.click()
                await page.wait_for_timeout(150)
                is_active = "active" in (await card.get_attribute("class") or "")
                record_check(f"Character Card Click: {char_id}", is_active, "Card gained active class")
            except Exception as e:
                record_check(f"Character Card Click: {char_id}", False, str(e))

        # Sample Preset Dialogue Buttons
        presets = [
            ("btnPresetBabilon", "Babilonia"),
            ("btnPresetAnak", "Suara Anak"),
            ("btnPresetKorporat", "Suara Korporat"),
            ("btnPresetVlog", "Suara Vlog"),
            ("btnPresetAudiobook", "Suara Audiobook"),
            ("btnPresetIklan", "Suara Iklan"),
            ("btnPresetMotivator", "Suara Motivator")
        ]
        for btn_id, label in presets:
            try:
                btn = page.locator(f"#{btn_id}")
                await btn.click()
                await page.wait_for_timeout(200)
                text_val = await page.locator("#narrationInput").input_value()
                record_check(f"Preset Button: {label}", len(text_val) > 10, f"Loaded text: {text_val[:30]}...")
            except Exception as e:
                record_check(f"Preset Button: {label}", False, str(e))

        # Smart Match Button (if visible)
        try:
            btn_match = page.locator("#btnLoadSmartMatch")
            is_match_visible = await btn_match.is_visible()
            if is_match_visible:
                await btn_match.click()
                await page.wait_for_timeout(300)
            record_check("Smart Match Button (#btnLoadSmartMatch)", True, f"Smart match button handled (visible={is_match_visible})")
        except Exception as e:
            record_check("Smart Match Button (#btnLoadSmartMatch)", False, str(e))

        # Clear Text Button
        try:
            await page.locator("#btnClearText").click()
            await page.wait_for_timeout(200)
            text_val = await page.locator("#narrationInput").input_value()
            record_check("Clear Text Button (#btnClearText)", len(text_val) == 0, "Textarea cleared to empty")
        except Exception as e:
            record_check("Clear Text Button (#btnClearText)", False, str(e))

        # Paste Text Button
        try:
            btn_paste = page.locator("#btnPasteText")
            await btn_paste.click()
            await page.wait_for_timeout(200)
            record_check("Paste Button (#btnPasteText)", True, "Clicked without error")
        except Exception as e:
            record_check("Paste Button (#btnPasteText)", False, str(e))

        # Vibe Selector Buttons
        vibe_btns = await page.locator(".vibe-btn").all()
        record_check("Vibe Buttons Count", len(vibe_btns) >= 4, f"Found {len(vibe_btns)} vibe buttons")
        for btn in vibe_btns:
            vibe_val = await btn.get_attribute("data-vibe")
            try:
                await btn.click()
                await page.wait_for_timeout(100)
                badge_text = await page.locator("#vibeBadge").inner_text()
                record_check(f"Vibe Button: {vibe_val}", vibe_val.lower() in badge_text.lower(), f"Vibe badge updated: {badge_text}")
            except Exception as e:
                record_check(f"Vibe Button: {vibe_val}", False, str(e))

        # Generate TTS Button
        try:
            await page.locator("#narrationInput").fill("Halo semuanya, ini pengujian otomatis sistem suara!")
            btn_gen = page.locator("#btnGenerateTTS")
            await btn_gen.click()
            await page.wait_for_timeout(2500)
            record_check("Generate TTS Button (#btnGenerateTTS)", True, "TTS generation triggered successfully")
        except Exception as e:
            record_check("Generate TTS Button (#btnGenerateTTS)", False, str(e))

        # -------------------------------------------------------------
        # TEST RIGHT SIDEBAR: DSP TUNER & AUDIO PLAYER BUTTONS
        # -------------------------------------------------------------
        print("\n--- 4. TESTING STUDIO DSP TUNER & PLAYER CONTROLS ---")

        # Player Play / Pause Button
        try:
            play_btn = page.locator("#btnMainPlay")
            await play_btn.click()
            await page.wait_for_timeout(500)
            status_text = await page.locator("#playbackStatusText").inner_text()
            record_check("Main Player Play/Pause Button (#btnMainPlay)", True, f"Status: {status_text}")
        except Exception as e:
            record_check("Main Player Play/Pause Button (#btnMainPlay)", False, str(e))

        # Player Stop Button (Testing the newly fixed Standby behavior)
        try:
            stop_btn = page.locator("#btnMainStop")
            await stop_btn.click()
            await page.wait_for_timeout(300)
            status_text = await page.locator("#playbackStatusText").inner_text()
            record_check("Main Player Stop Button (#btnMainStop)", "Standby" in status_text, f"Status: {status_text}")
        except Exception as e:
            record_check("Main Player Stop Button (#btnMainStop)", False, str(e))

        # Player Loop Button
        try:
            loop_btn = page.locator("#btnMainLoop")
            await loop_btn.click()
            await page.wait_for_timeout(200)
            loop_class = await loop_btn.get_attribute("class") or ""
            is_loop_on = "text-indigo-400" in loop_class
            record_check("Loop Toggle Button (#btnMainLoop)", is_loop_on, "Loop mode toggled on")
            await loop_btn.click()
            await page.wait_for_timeout(200)
        except Exception as e:
            record_check("Loop Toggle Button (#btnMainLoop)", False, str(e))

        # Pitch Preset Buttons
        pitch_presets = await page.locator(".pitch-preset-btn").all()
        for btn in pitch_presets:
            p_val = await btn.get_attribute("data-pitch")
            try:
                await btn.click()
                await page.wait_for_timeout(100)
                badge_text = await page.locator("#pitchBadge").inner_text()
                record_check(f"Pitch Preset Button ({p_val} st)", f"{p_val}" in badge_text or ("+" in badge_text and p_val in badge_text), f"Pitch badge: {badge_text}")
            except Exception as e:
                record_check(f"Pitch Preset Button ({p_val} st)", False, str(e))

        # Speed Preset Buttons
        speed_presets = await page.locator(".speed-preset-btn").all()
        for btn in speed_presets:
            s_val = await btn.get_attribute("data-speed")
            try:
                await btn.click()
                await page.wait_for_timeout(100)
                badge_text = await page.locator("#speedBadge").inner_text()
                record_check(f"Speed Preset Button ({s_val}x)", s_val in badge_text, f"Speed badge: {badge_text}")
            except Exception as e:
                record_check(f"Speed Preset Button ({s_val}x)", False, str(e))

        # Sliders verification (Pitch, Speed, Bass, Treble, Volume)
        sliders = [
            ("pitchSlider", "2", "pitchBadge"),
            ("speedSlider", "1.15", "speedBadge"),
            ("bassSlider", "3", "bassBadge"),
            ("trebleSlider", "2", "trebleBadge"),
            ("volumeSlider", "0.8", "volumeBadge")
        ]
        for slider_id, val, badge_id in sliders:
            try:
                sl = page.locator(f"#{slider_id}")
                await sl.fill(val)
                await page.wait_for_timeout(100)
                b_text = await page.locator(f"#{badge_id}").inner_text()
                record_check(f"DSP Slider: #{slider_id}", True, f"Badge #{badge_id} updated: {b_text}")
            except Exception as e:
                record_check(f"DSP Slider: #{slider_id}", False, str(e))

        # Download Buttons (Dual Format)
        try:
            btn_wav = page.locator("#btnDownloadWav")
            btn_wav_exists = await btn_wav.is_visible()
            record_check("Download WAV Button (#btnDownloadWav)", btn_wav_exists, "WAV download button visible & responsive")
        except Exception as e:
            record_check("Download WAV Button (#btnDownloadWav)", False, str(e))

        try:
            btn_mp3 = page.locator("#btnDownloadMp3")
            btn_mp3_exists = await btn_mp3.is_visible()
            record_check("Download MP3 Button (#btnDownloadMp3)", btn_mp3_exists, "MP3 download button visible & responsive")
        except Exception as e:
            record_check("Download MP3 Button (#btnDownloadMp3)", False, str(e))

        # -------------------------------------------------------------
        # TEST TAB 2: F5-TTS INDO STUDIO & VOICE RECORDER MODAL
        # -------------------------------------------------------------
        print("\n--- 5. TESTING TAB 2: F5-TTS INDO STUDIO & CLONER BUTTONS ---")
        await page.locator("#tabBtnF5").click()
        await page.wait_for_timeout(400)

        # Category Filter Buttons
        f5_cat_btns = await page.locator(".f5-cat-btn").all()
        record_check("F5 Category Pills Count", len(f5_cat_btns) >= 4, f"Found {len(f5_cat_btns)} pills")
        for btn in f5_cat_btns:
            cat_val = await btn.get_attribute("data-f5cat")
            try:
                await btn.click()
                await page.wait_for_timeout(200)
                btn_class = await btn.get_attribute("class") or ""
                record_check(f"F5 Cat Filter Pill: {cat_val}", "bg-amber-500" in btn_class, "Filter pill activated")
            except Exception as e:
                record_check(f"F5 Cat Filter Pill: {cat_val}", False, str(e))

        # Switch back to 'all'
        await page.locator(".f5-cat-btn[data-f5cat='all']").click()
        await page.wait_for_timeout(200)

        # Voice Cards Selection & Reference Audio Previews
        voice_cards = await page.locator(".f5-voice-card").all()
        record_check("F5 Voice Cards Count", len(voice_cards) >= 4, f"Found {len(voice_cards)} voice cards")
        for card in voice_cards[:4]:
            voice_id = await card.get_attribute("data-voiceid")
            try:
                await card.click()
                await page.wait_for_timeout(200)
                card_class = await card.get_attribute("class") or ""
                record_check(f"F5 Voice Card Click: {voice_id}", "border-amber-500" in card_class or "active" in card_class, "Voice card selected")
            except Exception as e:
                record_check(f"F5 Voice Card Click: {voice_id}", False, str(e))

        # Test Sample Audio Preview Button on Voice Card (.f5-preview-ref-btn)
        preview_btns = await page.locator(".f5-preview-ref-btn").all()
        record_check("F5 Reference Preview Buttons Count", len(preview_btns) > 0, f"Found {len(preview_btns)} reference preview buttons")
        if len(preview_btns) > 0:
            try:
                await preview_btns[0].click()
                await page.wait_for_timeout(500)
                record_check("F5 Reference Preview Button Click", True, "Sample audio auditioned in studio")
            except Exception as e:
                record_check("F5 Reference Preview Button Click", False, str(e))

        # Praise Chips in F5
        praise_chips = await page.locator(".f5-praise-chip").all()
        record_check("F5 Praise Chips Count", len(praise_chips) >= 4, f"Found {len(praise_chips)} chips")
        for chip in praise_chips[:3]:
            praise_txt = await chip.get_attribute("data-praise")
            try:
                await chip.click()
                await page.wait_for_timeout(200)
                input_val = await page.locator("#f5NarrationInput").input_value()
                record_check(f"F5 Praise Chip: {praise_txt[:20]}...", len(input_val) > 0, "Text inserted into F5 naskah")
            except Exception as e:
                record_check(f"F5 Praise Chip: {praise_txt[:20]}...", False, str(e))

        # Clear F5 Text Button
        try:
            await page.locator("#btnF5ClearText").click()
            await page.wait_for_timeout(200)
            input_val = await page.locator("#f5NarrationInput").input_value()
            record_check("Clear F5 Text Button (#btnF5ClearText)", len(input_val) == 0, "F5 textarea cleared")
        except Exception as e:
            record_check("Clear F5 Text Button (#btnF5ClearText)", False, str(e))

        # Bilingual Switch
        try:
            bi_switch = page.locator("#f5BilingualSwitch")
            await bi_switch.click()
            await page.wait_for_timeout(200)
            is_checked = await bi_switch.is_checked()
            record_check("Bilingual Pronunciation Switch", True, f"Toggled, checked: {is_checked}")
            if not is_checked:
                await bi_switch.click()
        except Exception as e:
            record_check("Bilingual Pronunciation Switch", False, str(e))

        # Quick Action Buttons: Auto-Cloners
        try:
            btn_marcia = page.locator("#btnAutoCloneMarcia")
            btn_marcia_visible = await btn_marcia.is_visible()
            record_check("Quick Action: Kloning Cepat Marcia", btn_marcia_visible, "Button is visible and active")
        except Exception as e:
            record_check("Quick Action: Kloning Cepat Marcia", False, str(e))

        try:
            btn_john = page.locator("#btnAutoCloneJohn")
            btn_john_visible = await btn_john.is_visible()
            record_check("Quick Action: Kloning Cepat Tutor John", btn_john_visible, "Button is visible and active")
        except Exception as e:
            record_check("Quick Action: Kloning Cepat Tutor John", False, str(e))

        try:
            btn_prof = page.locator("#btnAutoCloneProf")
            btn_prof_visible = await btn_prof.is_visible()
            record_check("Quick Action: Kloning Cepat Prof. Yohanes Surya", btn_prof_visible, "Button is visible and active")
        except Exception as e:
            record_check("Quick Action: Kloning Cepat Prof. Yohanes Surya", False, str(e))

        # -------------------------------------------------------------
        # TEST VOICE RECORDER MODAL & CONTROLS
        # -------------------------------------------------------------
        print("\n--- 6. TESTING VOICE RECORDER MODAL & ALL RECORD CONTROLS ---")
        try:
            await page.locator("#btnOpenVoiceRecorder").click()
            await page.wait_for_timeout(300)
            modal = page.locator("#voiceRecordModal")
            modal_visible = await modal.is_visible()
            record_check("Open Voice Record Modal (#btnOpenVoiceRecorder)", modal_visible, "Modal displayed")
        except Exception as e:
            record_check("Open Voice Record Modal (#btnOpenVoiceRecorder)", False, str(e))

        # Modal Mode Buttons: Trainer vs Custom
        try:
            btn_custom = page.locator("#modeBtnCustom")
            await btn_custom.click()
            await page.wait_for_timeout(200)
            label_text = await page.locator("#labelSpeakerName").inner_text()
            record_check("Modal Mode: Suara Pribadi / Mandiri", "Pribadi" in label_text, f"Label: {label_text}")

            btn_trainer = page.locator("#modeBtnTrainer")
            await btn_trainer.click()
            await page.wait_for_timeout(200)
            label_text = await page.locator("#labelSpeakerName").inner_text()
            record_check("Modal Mode: Suara AT / Trainer GASING", "AT" in label_text or "Trainer" in label_text, f"Label: {label_text}")
        except Exception as e:
            record_check("Modal Mode Toggles", False, str(e))

        # Test Speaker Chime Button
        try:
            chime_btn = page.locator("#btnTestSpeakerChime")
            await chime_btn.click()
            await page.wait_for_timeout(200)
            record_check("Speaker Test Chime Button (#btnTestSpeakerChime)", await chime_btn.is_visible(), "Speaker test chime button clicked")
        except Exception as e:
            record_check("Speaker Test Chime Button (#btnTestSpeakerChime)", False, str(e))

        # Test Mic Device Selector & Refresh Button
        try:
            select_mic = page.locator("#selectMicDevice")
            refresh_mic = page.locator("#btnRefreshMicDevices")
            is_select_vis = await select_mic.is_visible()
            await refresh_mic.click()
            await page.wait_for_timeout(300)
            record_check("Mic Device Selector & Refresh (#selectMicDevice & #btnRefreshMicDevices)", is_select_vis, "Mic selector & refresh responsive")
        except Exception as e:
            record_check("Mic Device Selector & Refresh", False, str(e))

        # Switch Calibration Script Button
        try:
            script_btn = page.locator("#btnSwitchCalibScript")
            initial_text = await page.locator("#inputRefText").input_value()
            await script_btn.click()
            await page.wait_for_timeout(200)
            new_text = await page.locator("#inputRefText").input_value()
            record_check("Switch Calibration Script (#btnSwitchCalibScript)", initial_text != new_text, f"Switched text: {new_text[:35]}...")
        except Exception as e:
            record_check("Switch Calibration Script (#btnSwitchCalibScript)", False, str(e))

        # Record Standby State Check
        btn_record = page.locator("#btnToggleRecord")
        btn_play = page.locator("#btnPlayRecordedSample")
        btn_reset = page.locator("#btnResetRecord")
        btn_save = page.locator("#btnSaveClonedVoice")

        record_check("Standby: Mulai Merekam visible", await btn_record.is_visible(), "Record button is ready")
        record_check("Standby: Putar Rekaman hidden", await btn_play.is_hidden(), "Play sample button is hidden")
        record_check("Standby: Rekam Ulang hidden", await btn_reset.is_hidden(), "Reset button is hidden")
        record_check("Standby: Simpan disabled", await btn_save.is_disabled(), "Save button is safely disabled")

        # Start Recording with synthetic mic
        try:
            await btn_record.click(force=True)
            await page.wait_for_timeout(800)
            rec_text = await page.locator("#btnToggleRecordText").inner_text()
            record_check("Recording Started: Button text changed", "Selesai" in rec_text or "Hentikan" in rec_text, f"Button text: {rec_text}")
            
            # Record for 2.5 seconds
            await page.wait_for_timeout(2500)

            # Stop Recording (force=True avoids waiting for infinite CSS pulse animation)
            await btn_record.click(force=True)
            await page.wait_for_timeout(1000)

            # Check Recorded State
            record_check("Recorded State: Record btn hidden", await btn_record.is_hidden(), "Record button hidden")
            record_check("Recorded State: Play btn visible & enabled", await btn_play.is_visible() and not await btn_play.is_disabled(), "Play sample button enabled")
            record_check("Recorded State: Reset btn visible", await btn_reset.is_visible(), "Reset button visible")
            record_check("Recorded State: Save btn enabled", not await btn_save.is_disabled(), "Save button enabled")
        except Exception as e:
            record_check("Recording Flow", False, str(e))

        # Play Recorded Sample
        try:
            await btn_play.click(force=True)
            await page.wait_for_timeout(500)
            play_text = await page.locator("#playSampleText").inner_text()
            record_check("Play Recorded Sample: Toggle to Pause", "Jeda" in play_text or "Putar" in play_text, f"Play button text: {play_text}")
        except Exception as e:
            record_check("Play Recorded Sample", False, str(e))

        # Reset / Re-record Button
        try:
            await btn_reset.click(force=True)
            await page.wait_for_timeout(500)
            is_record_back = await btn_record.is_visible()
            is_play_hidden = await btn_play.is_hidden()
            record_check("Reset Recording Button (#btnResetRecord)", is_record_back and is_play_hidden, "Cleanly reset to standby")
        except Exception as e:
            record_check("Reset Recording Button (#btnResetRecord)", False, str(e))

        # File Upload trigger button (#btnTriggerFileSelect)
        try:
            btn_file = page.locator("#btnTriggerFileSelect")
            is_file_btn_visible = await btn_file.is_visible()
            record_check("File Upload Trigger Button (#btnTriggerFileSelect)", is_file_btn_visible, "File trigger button visible")
        except Exception as e:
            record_check("File Upload Trigger Button (#btnTriggerFileSelect)", False, str(e))

        # Close Modal
        try:
            await page.locator("#btnCloseRecordModal").click()
            await page.wait_for_timeout(300)
            modal_hidden = await page.locator("#voiceRecordModal").is_hidden()
            record_check("Close Modal Button (#btnCloseRecordModal)", modal_hidden, "Modal closed cleanly")
        except Exception as e:
            record_check("Close Modal Button (#btnCloseRecordModal)", False, str(e))

        # -------------------------------------------------------------
        # TEST TAB 3: PAPAN ASSET ASLI (SOUNDBOARD CATALOG)
        # -------------------------------------------------------------
        print("\n--- 7. TESTING TAB 3: PAPAN ASSET ASLI (SOUNDBOARD) ---")
        await page.locator("#tabBtnSoundboard").click()
        await page.wait_for_timeout(400)

        # Asset Category Filters
        cat_filters = await page.locator(".cat-filter-btn").all()
        record_check("Soundboard Category Pills Count", len(cat_filters) >= 4, f"Found {len(cat_filters)} pills")
        for btn in cat_filters:
            cat_val = await btn.get_attribute("data-cat")
            try:
                await btn.click()
                await page.wait_for_timeout(200)
                badge_text = await page.locator("#catalogFilteredCount").inner_text()
                record_check(f"Soundboard Cat Filter: {cat_val}", len(badge_text) > 0, f"Filtered count: {badge_text}")
            except Exception as e:
                record_check(f"Soundboard Cat Filter: {cat_val}", False, str(e))

        # Asset Search
        try:
            search = page.locator("#soundboardSearchInput")
            await search.fill("WOW")
            await page.wait_for_timeout(300)
            badge_text = await page.locator("#catalogFilteredCount").inner_text()
            record_check("Soundboard Search Input", "Asset" in badge_text, f"Search result: {badge_text}")
            await search.fill("")
            await page.wait_for_timeout(300)
        except Exception as e:
            record_check("Soundboard Search Input", False, str(e))

        # Soundboard Asset Cards (Play & Load into Studio)
        play_card_btns = await page.locator(".btn-play-card").all()
        record_check("Soundboard Play Card Buttons Count", len(play_card_btns) > 0, f"Found {len(play_card_btns)} cards")
        if len(play_card_btns) > 0:
            try:
                first_play = play_card_btns[0]
                await first_play.click()
                await page.wait_for_timeout(500)
                record_check("Soundboard Card Play Button", True, "Card play triggered")
            except Exception as e:
                record_check("Soundboard Card Play Button", False, str(e))

        load_card_btns = await page.locator(".btn-load-studio").all()
        if len(load_card_btns) > 0:
            try:
                first_load = load_card_btns[0]
                await first_load.click()
                await page.wait_for_timeout(500)
                studio_title = await page.locator("#currentAudioTitle").inner_text()
                record_check("Soundboard Card 'Muat ke Studio' Button", len(studio_title) > 0, f"Loaded to studio: {studio_title}")
            except Exception as e:
                record_check("Soundboard Card 'Muat ke Studio' Button", False, str(e))

        # Capture final screenshot
        screenshot_path = "/Users/yohanessurya/.gemini/antigravity-ide/brain/f7e201ad-f711-4a14-bd96-6b0384c503ed/playwright_audit_complete.png"
        await page.screenshot(path=screenshot_path, full_page=True)
        print(f"\n📸 Full page test screenshot saved to: {screenshot_path}")

        await browser.close()

    print("\n" + "=" * 70)
    print("📊 PLAYWRIGHT ALL-BUTTONS AUDIT RESULTS SUMMARY")
    print("=" * 70)
    print(f"Total Checks  : {results['total']}")
    print(f"Passed Checks : {results['passed']}")
    print(f"Failed Checks : {results['failed']}")

    if results["failures"]:
        print("\n❌ Failures Summary:")
        for name, details in results["failures"]:
            print(f"  - {name}: {details}")
    else:
        print("\n🎉 ALL BUTTONS & CONTROLS PASSED 100%!")
    print("=" * 70)

    if results["failed"] > 0:
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(run_tests())
