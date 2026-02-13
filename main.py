#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys
import csv
import json
import locale
import shutil
from pathlib import Path


if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def get_system_language():
    lang = os.environ.get('LANG', '')
    if 'zh' in lang.lower() or 'chinese' in lang.lower():
        return 'zh_CN'
    try:
        locale.setlocale(locale.LC_ALL, '')
        lang = locale.getlocale()[0]
        if lang and ('zh' in lang.lower() or 'chinese' in lang.lower()):
            return 'zh_CN'
    except:
        pass
    return 'en_US'


def load_messages(lang='en_US'):
    locale_dir = Path(__file__).parent / 'locales'
    locale_file = locale_dir / f'{lang}.json'
    if not locale_file.exists():
        lang = 'en_US'
        locale_file = locale_dir / 'en_US.json'
    try:
        if locale_file.exists():
            with open(locale_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Warning: Failed to load locale file {locale_file}: {e}")
    return {
        'usage': 'Usage:',
        'usage_func1': '  python main.py 1  - Execute Function 1',
        'usage_func2': '  python main.py 2  - Execute Function 2',
        'unknown_function': 'Error: Unknown function parameter',
        'use_1_or_2': 'Please use 1 or 2',
    }


class IconGenerator:
    def __init__(self, lang='en_US'):
        self.input_dir = Path("input")
        self.map_dir = Path("map")
        self.output_dir = Path("output")
        self.templates_dir = Path("templates")
        self.data_csv = self.map_dir / "data.csv"
        self.lang = lang
        self.msg = load_messages(lang)
        
    def function1_add_to_data(self):
        print(self.msg['func1_start'])
        csv_files = list(self.input_dir.glob("*.csv"))
        if len(csv_files) == 0:
            print(self.msg['no_csv'])
            sys.exit(1)
        elif len(csv_files) > 1:
            print(self.msg['multiple_csv'].format(len(csv_files)))
            sys.exit(1)
        input_csv = csv_files[0]
        print(self.msg['found_input'].format(input_csv.name))
        try:
            with open(input_csv, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)
            if len(rows) < 1:
                print(self.msg['csv_empty'])
                sys.exit(1)
            header = rows[0]
            if len(header) != 3:
                print(self.msg['csv_wrong_columns'].format(len(header)))
                sys.exit(1)
            expected_header = ['AppName', 'PackageName', 'LauncherActivity']
            if header != expected_header:
                print(self.msg['csv_wrong_header'])
                print(self.msg['expected_header'].format(expected_header))
                print(self.msg['actual_header'].format(header))
                sys.exit(1)
            print(self.msg['csv_format_ok'])
            data_rows = rows[1:]
            for i, row in enumerate(data_rows, start=2):
                if len(row) != 3:
                    print(self.msg['row_wrong_columns'].format(i, len(row)))
                    sys.exit(1)
            print(self.msg['data_rows_ok'].format(len(data_rows)))
        except Exception as e:
            print(self.msg['read_input_error'].format(e))
            sys.exit(1)
        existing_data = {}
        if self.data_csv.exists():
            try:
                with open(self.data_csv, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    existing_rows = list(reader)
                for row in existing_rows[1:]:
                    if len(row) >= 3:
                        key = f"{row[1]}|{row[2]}"  # PackageName|LauncherActivity
                        existing_data[key] = row       
                print(self.msg['existing_records'].format(len(existing_data)))
            except Exception as e:
                print(self.msg['read_data_error'].format(e))
                sys.exit(1)
        else:
            print(self.msg['data_csv_not_exist'])
        new_rows = []
        for row in data_rows:
            key = f"{row[1]}|{row[2]}"
            if key not in existing_data:
                new_rows.append(row)
        if len(new_rows) == 0:
            print(self.msg['no_new_data'])
            return
        print(self.msg['new_data_found'].format(len(new_rows)))
        try:
            if not self.data_csv.exists():
                self.map_dir.mkdir(parents=True, exist_ok=True)
                with open(self.data_csv, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['AppName', 'PackageName', 'LauncherActivity', 'IconName'])
            with open(self.data_csv, 'a', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                for row in new_rows:
                    writer.writerow(row + [''])
                    print(f"  + {row[0]}")
            print(self.msg['add_success'].format(len(new_rows)))
            print(self.msg['fill_iconname'])
        except Exception as e:
            print(self.msg['write_data_error'].format(e))
            sys.exit(1)
    
    def function2_generate_output(self):
        print(self.msg['func2_start'])
        if not self.data_csv.exists():
            print(self.msg['data_csv_missing'])
            sys.exit(1)
        try:
            with open(self.data_csv, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)
            if len(rows) < 1:
                print(self.msg['data_csv_empty'])
                sys.exit(1)
            header = rows[0]
            if len(header) != 4:
                print(self.msg['data_wrong_columns'].format(len(header)))
                sys.exit(1)
            data_rows = rows[1:]
            print(self.msg['data_rows_count'].format(len(data_rows)))
            for i, row in enumerate(data_rows, start=2):
                if len(row) != 4:
                    print(self.msg['row_wrong_columns'].format(i, len(row)))
                    sys.exit(1)
                if not row[3] or row[3].strip() == '':
                    print(self.msg['iconname_empty'].format(i))
                    print(self.msg['app_name'].format(row[0]))
                    print(self.msg['fill_iconname_first'])
                    sys.exit(1)
            print(self.msg['all_iconname_filled'])
        except Exception as e:
            print(self.msg['read_data_error'].format(e))
            sys.exit(1)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        try:
            self._generate_appfilter(data_rows)
            self._generate_appmap(data_rows)
            self._generate_drawable(data_rows)
            self._generate_icon_pack(data_rows)
            self._generate_theme_resources(data_rows)
            print(self.msg['generate_success'])
        except Exception as e:
            print(self.msg['generate_error'].format(e))
            sys.exit(1)

    def _generate_appfilter(self, data_rows):
        output_file = self.output_dir / "appfilter.xml"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write('<resources>\n')
            f.write('\n')
            for row in data_rows:
                app_name, package_name, launcher_activity, icon_name = row
                f.write('    <item\n')
                f.write(f'        component="ComponentInfo{{{package_name}/{launcher_activity}}}"\n')
                f.write(f'        drawable="{icon_name}" />\n')
                f.write('\t\n')
            f.write('\n')
            f.write('</resources>')
        print(self.msg['generated_file'].format('appfilter.xml'))
    
    def _generate_appmap(self, data_rows):
        output_file = self.output_dir / "appmap.xml"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" ?>\n')
            f.write('<appmap>\n')
            for row in data_rows:
                app_name, package_name, launcher_activity, icon_name = row
                f.write(f'    <item class="{launcher_activity}" name="{icon_name}"/>\n')
            f.write('</appmap>\n')
        print(self.msg['generated_file'].format('appmap.xml'))
    
    def _generate_drawable(self, data_rows):
        output_file = self.output_dir / "drawable.xml"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" ?>\n')
            f.write('<resources>\n')
            f.write('    <version>1</version>\n')
            f.write('    <category title="icons"/>\n')
            for row in data_rows:
                app_name, package_name, launcher_activity, icon_name = row
                f.write(f'    <item drawable="{icon_name}"/>\n')
            f.write('</resources>\n')
        print(self.msg['generated_file'].format('drawable.xml'))
    
    def _generate_icon_pack(self, data_rows):
        output_file = self.output_dir / "icon_pack.xml"
        template_file = self.templates_dir / "icon_pack_template.xml"
        if template_file.exists():
            with open(template_file, 'r', encoding='utf-8') as f:
                template_content = f.read()
        else:
            print(self.msg['template_not_exist'])
            template_content = '''<?xml version="1.0" encoding="utf-8"?><!--suppress CheckTagEmptyBody -->
<resources xmlns:tools="http://schemas.android.com/tools" tools:ignore="ExtraTranslation">

    <string-array name="icons_preview">
        <item>dialer</item>
        <item>contacts</item>
        <item>messaging</item>
        <item>fossify_camera</item>
        <item>breezy_weather</item>
        <item>fossify_gallery</item>
        <item>calculator</item>
        <item>pyroscape</item>
        <item>settings</item>
    </string-array>

    <string-array name="icon_filters">
        <item>all</item>
    </string-array>

    <!-- The following content is automatically generated, please do not modify. -->
'''
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(template_content)
            f.write('    <string-array name="all">\n')
            
            for row in data_rows:
                app_name, package_name, launcher_activity, icon_name = row
                f.write(f'        <item>{icon_name}</item>\n')
            
            f.write('    </string-array>\n')
            f.write('</resources>')
        
        print(self.msg['generated_file'].format('icon_pack.xml'))
    
    def _generate_theme_resources(self, data_rows):
        output_file = self.output_dir / "theme_resources.xml"
        template_file = self.templates_dir / "theme_resources_template.xml"
        if template_file.exists():
            with open(template_file, 'r', encoding='utf-8') as f:
                template_content = f.read()
        else:
            print(self.msg['template_not_exist'])
            template_content = '''<?xml version="1.0" encoding="UTF-8"?>
<Theme version="1">
    <Label value="Blueprint" />
    <Wallpaper image="wallpaper_01" />
    <LockScreenWallpaper image="wallpaper_02" />
    <ThemePreview image="preview1" />
    <ThemePreviewWork image="preview1" />
    <ThemePreviewMenu image="preview1" />
    <DockMenuAppIcon selector="drawer" />

    <!-- The following content is automatically generated, please do not modify. -->
'''
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(template_content)
            for row in data_rows:
                app_name, package_name, launcher_activity, icon_name = row
                f.write(f'    <AppIcon name="{package_name}/{launcher_activity}" image="{icon_name}"/>\n')
            f.write('</Theme>')
        print(self.msg['generated_file'].format('theme_resources.xml'))
    
    def copy_xml_files(self,target_dir):
        if not os.path.isdir(target_dir):
            print(self.msg['target_dir_not_exist'].format(target_dir))
            sys.exit(1)
        xml_dir = os.path.join(target_dir, 'app', 'src', 'main', 'res', 'xml')
        assets_dir = os.path.join(target_dir, 'app', 'src', 'main', 'assets')
        missing_dirs = []
        if not os.path.isdir(xml_dir):
            missing_dirs.append(xml_dir)
        if not os.path.isdir(assets_dir):
            missing_dirs.append(assets_dir)
        if missing_dirs:
            print(self.msg['following_dir_not_exist'])
            for d in missing_dirs:
                print(f"  {d}")
            sys.exit(1)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        source_dir = os.path.join(script_dir, 'output')
        if not os.path.isdir(source_dir):
            print(self.msg['source_dir_not_exist'].format(source_dir))
            sys.exit(1)
        required_files = [
            'appfilter.xml',
            'appmap.xml',
            'drawable.xml',
            'icon_pack.xml',
            'theme_resources.xml'
        ]
        missing_files = []
        for f in required_files:
            file_path = os.path.join(source_dir, f)
            if not os.path.isfile(file_path):
                missing_files.append(f)
        if missing_files:
            print(self.msg['following_file_not_exist'])
            for f in missing_files:
                print(f"  {f}")
            sys.exit(1)
        print(self.msg['func4_start'])
        for f in required_files:
            src = os.path.join(source_dir, f)
            dst_xml = os.path.join(xml_dir, f)
            shutil.copy2(src, dst_xml)
            print(self.msg['copy_completed'].format(dst_xml))
            dst_assets = os.path.join(assets_dir, f)
            shutil.copy2(src, dst_assets)
            print(self.msg['copy_completed'].format(dst_assets))
        print(self.msg['func4_completed'])

    def read_target_from_config(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, 'config', 'config.json')
        if not os.path.isfile(config_path):
            print(self.msg['config_file_not_exist'].format(config_path))
            sys.exit(1)
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except json.JSONDecodeError as e:
            print(self.msg['config_wrong_format'].format(e))
            sys.exit(1)
        target_dir = config.get('target_dir')
        if not target_dir:
            print(self.msg['config_target_dir_missing'])
            sys.exit(1)
        return target_dir


def main():
    lang = get_system_language()
    msg = load_messages(lang)
    if len(sys.argv) < 2:
        print(msg['usage'])
        print(msg['usage_func1'])
        print(msg['usage_func2'])
        print(msg['usage_func4_1'])
        print(msg['usage_func4_2'])
        print(msg['usage_func3'])
        sys.exit(1)
    function = sys.argv[1]
    generator = IconGenerator(lang)
    if function == "-a":
        generator.function1_add_to_data()
    elif function == "-g":
        generator.function2_generate_output()
    elif function == "-h":
        print(msg['usage'])
        print(msg['usage_func1'])
        print(msg['usage_func2'])
        print(msg['usage_func4_1'])
        print(msg['usage_func4_2'])
        print(msg['usage_func3'])
        sys.exit(1)
    elif function == "-c":
        if len(sys.argv) == 3:
            target = sys.argv[2]
        elif len(sys.argv) == 2:
            print(msg['read_from_config'])
            target = generator.read_target_from_config()
        else:
            print(msg['copy_incorrect_argument'])
            print(msg['usage'])
            print(msg['usage_func4_1'])
            print(msg['usage_func4_2'])
            sys.exit(1)
        generator.copy_xml_files(target)
    else:
        print(msg['unknown_function'].format(function))
        print(msg['use_1_or_2'])
        sys.exit(1)


if __name__ == "__main__":
    main()
