#!/usr/bin/env python3
"""
Markdown 파일 변환 스크립트
content/ 디렉토리의 파일들을 _posts/ 형식으로 변환
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime
import yaml

# 경로 설정
BASE_DIR = Path(__file__).parent
CONTENT_DIR = BASE_DIR / "content"
POSTS_DIR = BASE_DIR / "_posts"
ASSETS_DIR = BASE_DIR / "assets" / "img" / "for_post"

def parse_frontmatter(content):
    """Front matter 파싱"""
    match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
    if not match:
        return None, content

    frontmatter_str = match.group(1)
    body = match.group(2)

    try:
        frontmatter = yaml.safe_load(frontmatter_str)
    except yaml.YAMLError:
        return None, content

    return frontmatter, body

def convert_date_format(date_str):
    """날짜 형식 변환: 'YYYY-MM-DD HH:MM:SS' → YYYY-MM-DD HH:MM:SS +/-TTTT"""
    if not date_str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S +/-TTTT")

    # 따옴표 제거
    date_str = str(date_str).strip("'\"")

    # 이미 올바른 형식인지 확인
    if '+/-TTTT' in date_str or '+0900' in date_str:
        return date_str

    # 'YYYY-MM-DD HH:MM:SS' 형식 처리
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%Y-%m-%d %H:%M:%S +/-TTTT")
    except ValueError:
        pass

    # 'YYYY-MM-DD' 형식 처리
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%Y-%m-%d 12:00:00 +/-TTTT")
    except ValueError:
        pass

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S +/-TTTT")

def convert_categories_tags(value):
    """categories/tags를 배열 형식으로 변환"""
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        # 쉼표로 구분된 문자열을 배열로 변환
        return [item.strip() for item in value.split(',')]
    return [str(value)]

def extract_date_from_path(dir_path):
    """디렉토리명에서 날짜 추출"""
    dir_name = os.path.basename(dir_path)

    # "YYYY.MM.DD Title" 형식
    date_match = re.match(r'^(\d{4})\.(\d{2})\.(\d{2})\s+', dir_name)
    if date_match:
        year, month, day = date_match.groups()
        return f"{year}-{month}-{day}"

    return None

def generate_slug(title, dir_name):
    """제목에서 slug 생성"""
    # 날짜 제거 후 나머지 부분 사용
    slug = re.sub(r'^\d{4}\.\d{2}\.\d{2}\s+', '', dir_name)

    # 영문이 있으면 영문 사용
    if re.search(r'[a-zA-Z]', slug):
        slug = re.sub(r'[^a-zA-Z0-9\s-]', '', slug)
        slug = re.sub(r'\s+', '-', slug.strip())
        slug = slug.lower()[:50]
        return slug

    # 한글만 있으면 제목의 일부를 음역하거나 숫자 사용
    # 간단하게 디렉토리명의 해시값 사용
    import hashlib
    hash_val = hashlib.md5(dir_name.encode()).hexdigest()[:8]
    return hash_val

def convert_image_paths(body, source_dir, date_str):
    """이미지 경로 변환 및 파일 복사"""
    date_prefix = date_str.split()[0]  # YYYY-MM-DD 부분만

    # 이미지 참조 패턴 찾기: ![alt](image.ext) 또는 ![](image.ext)
    def replace_image(match):
        alt_text = match.group(1)
        img_filename = match.group(2)

        # 이미 절대 경로이거나 http로 시작하면 그대로 유지
        if img_filename.startswith('/') or img_filename.startswith('http'):
            return match.group(0)

        # 원본 이미지 파일 경로
        source_img = source_dir / img_filename

        if source_img.exists():
            # 새 이미지 파일명: YYYY-MM-DD-imageName.ext
            img_ext = source_img.suffix
            img_base = source_img.stem

            # 이미 날짜 프리픽스가 있는지 확인
            if not img_base.startswith(date_prefix):
                new_img_name = f"{date_prefix}-{img_base}{img_ext}"
            else:
                new_img_name = f"{img_base}{img_ext}"

            # assets/img/for_post/로 복사
            dest_img = ASSETS_DIR / new_img_name

            try:
                if not dest_img.exists():
                    shutil.copy2(source_img, dest_img)
                    print(f"  ✓ 이미지 복사: {img_filename} -> {new_img_name}")

                # 이미지 경로를 파일명만으로 변경 (img_path 기준)
                return f"![{alt_text}]({new_img_name})"
            except Exception as e:
                print(f"  ⚠ 이미지 복사 실패: {img_filename} - {e}")
                return match.group(0)
        else:
            print(f"  ⚠ 이미지 파일 없음: {source_img}")
            return match.group(0)

    # 이미지 패턴 치환
    body = re.sub(r'!\[(.*?)\]\(([^)]+)\)', replace_image, body)

    return body

def clean_body(body):
    """본문 정리"""
    # ```toc``` 제거
    body = re.sub(r'```toc\s*```', '', body)

    # <br >, <br/>, <br> 태그 제거 또는 빈 줄로 변환
    body = re.sub(r'<br\s*/?>(\s*\n)?', '\n', body)

    # 연속된 빈 줄 정리 (3개 이상 -> 2개)
    body = re.sub(r'\n{3,}', '\n\n', body)

    return body.strip()

def create_frontmatter(original_fm, dir_name, date_str):
    """새로운 front matter 생성"""
    new_fm = {
        'title': original_fm.get('title', dir_name),
        'date': convert_date_format(original_fm.get('date', date_str)),
        'categories': convert_categories_tags(original_fm.get('categories', 'WIKI')),
        'tags': convert_categories_tags(original_fm.get('tags', '')),
        'math': True,
        'toc': True,
        'author': original_fm.get('author', 'j-ho'),
        'img_path': '/assets/img/for_post/',
        'pin': False,
        'description': original_fm.get('description', original_fm.get('title', ''))
    }

    return new_fm

def convert_post(source_dir):
    """개별 포스트 변환"""
    index_file = source_dir / "index.md"

    if not index_file.exists():
        print(f"⚠ index.md 없음: {source_dir}")
        return False

    # 파일 읽기
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Front matter 파싱
    frontmatter, body = parse_frontmatter(content)

    if frontmatter is None:
        print(f"⚠ Front matter 파싱 실패: {source_dir}")
        return False

    dir_name = os.path.basename(source_dir)

    # 날짜 추출
    date_from_path = extract_date_from_path(source_dir)
    date_str = date_from_path or frontmatter.get('date', datetime.now().strftime("%Y-%m-%d"))

    # Slug 생성
    slug = generate_slug(frontmatter.get('title', dir_name), dir_name)

    # 새 파일명
    new_filename = f"{date_str.split()[0]}-{slug}.md"

    # 이미지 경로 변환
    body = convert_image_paths(body, source_dir, date_str)

    # 본문 정리
    body = clean_body(body)

    # 새 front matter 생성
    new_frontmatter = create_frontmatter(frontmatter, dir_name, date_str)

    # 새 파일 내용 생성
    new_content = "---\n"
    new_content += yaml.dump(new_frontmatter, allow_unicode=True, default_flow_style=False)
    new_content += "---\n\n"
    new_content += body

    # _posts 디렉토리에 저장
    output_file = POSTS_DIR / new_filename

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"✓ 변환 완료: {dir_name} -> {new_filename}")
    return True

def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("Markdown 파일 변환 시작")
    print("=" * 60)

    # _posts 디렉토리 확인
    POSTS_DIR.mkdir(exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    # content 디렉토리의 모든 하위 디렉토리 탐색
    content_dirs = [d for d in CONTENT_DIR.iterdir() if d.is_dir()]

    success_count = 0
    fail_count = 0

    for content_dir in sorted(content_dirs):
        print(f"\n처리 중: {content_dir.name}")
        if convert_post(content_dir):
            success_count += 1
        else:
            fail_count += 1

    print("\n" + "=" * 60)
    print(f"변환 완료: 성공 {success_count}개, 실패 {fail_count}개")
    print("=" * 60)

if __name__ == "__main__":
    main()
